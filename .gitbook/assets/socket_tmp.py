#!/usr/bin/env python3
"""Find non-default Unix sockets, pick one, read it (incl. SCM_RIGHTS FDs)."""
import argparse, array, fnmatch, os, socket, stat, sys
 
DEFAULTS = ["/run/systemd/*", "/run/udev/*", "/run/dbus/*", "/var/run/dbus/*",
            "/run/user/*", "/dev/log", "/run/initctl", "/run/lvm/*",
            "/run/dmeventd-*", "/run/mdadm/*", "/run/rpcbind.sock"]
SCAN = ["/run", "/var/run", "/tmp", "/dev", "/var/lib"]
PRUNE = {"/proc", "/sys"}
TYPES = {"0001": socket.SOCK_STREAM, "0002": socket.SOCK_DGRAM, "0005": socket.SOCK_SEQPACKET}
LABEL = {socket.SOCK_STREAM: "STREAM", socket.SOCK_DGRAM: "DGRAM", socket.SOCK_SEQPACKET: "SEQPACKET"}
 
 
def proc_unix():
    types = {}
    try:
        with open("/proc/net/unix") as f:
            next(f, None)
            for line in f:
                p = line.split()
                if len(p) >= 8 and p[-1].startswith("/"):
                    types[p[-1]] = TYPES.get(p[4])
    except OSError:
        pass
    return types
 
 
def walk(paths):
    found = set()
    for root in paths:
        for dp, dns, fns in os.walk(root, onerror=lambda e: None, followlinks=False):
            dns[:] = [d for d in dns if os.path.join(dp, d) not in PRUNE]
            for n in fns:
                f = os.path.join(dp, n)
                try:
                    if stat.S_ISSOCK(os.lstat(f).st_mode):
                        found.add(f)
                except OSError:
                    pass
    return found
 
 
def discover(paths, include_default):
    allp = proc_unix()
    for p in walk(paths):
        allp.setdefault(p, None)
    out = []
    for path, t in sorted(allp.items()):
        if not include_default and any(fnmatch.fnmatch(path, g) for g in DEFAULTS):
            continue
        out.append({"path": path, "r": os.access(path, os.R_OK),
                    "w": os.access(path, os.W_OK), "type": t})
    return out
 
 
def connect(path, timeout, pref=None):
    order = ([pref] if pref else []) + [t for t in (socket.SOCK_STREAM, socket.SOCK_SEQPACKET, socket.SOCK_DGRAM) if t != pref]
    err = None
    for t in order:
        s = socket.socket(socket.AF_UNIX, t)
        s.settimeout(timeout)
        try:
            s.connect(path)
            return s, t
        except OSError as e:
            err, _ = e, s.close()
    raise err
 
 
def recv_fds(s, max_fds, bufsize):
    fds = array.array("i")
    msg, anc, flags, _ = s.recvmsg(bufsize, socket.CMSG_SPACE(max_fds * fds.itemsize))
    if flags & socket.MSG_CTRUNC:
        print("WARN: ancillary data truncated; raise --max-fds", file=sys.stderr)
    for lvl, typ, data in anc:
        if lvl == socket.SOL_SOCKET and typ == socket.SCM_RIGHTS:
            fds.frombytes(data[:len(data) - len(data) % fds.itemsize])
    return msg, list(fds)
 
 
def read_fd(fd, chunk):
    buf, off, seek = [], 0, True
    while True:
        try:
            d = os.pread(fd, chunk, off) if seek else os.read(fd, chunk)
        except OSError:
            if seek:
                seek = False; continue
            raise
        if not d:
            break
        buf.append(d); off += len(d)
    return b"".join(buf)
 
 
def read_socket(path, a, pref=None):
    print(f"[*] connecting {path}")
    try:
        s, t = connect(path, a.timeout, pref)
    except OSError as e:
        print(f"ERR connect: {e}", file=sys.stderr); return 1
    print(f"[*] connected {LABEL.get(t, '?')}")
    try:
        try:
            msg, fds = recv_fds(s, a.max_fds, a.msg_bufsize)
        except socket.timeout:
            print("ERR: timed out (socket sent nothing)", file=sys.stderr); return 1
        except OSError as e:
            print(f"ERR recvmsg: {e}", file=sys.stderr); return 1
        print("MSG:", msg.decode(errors="replace"))
        if not fds:
            print("no FDs received"); return 0
        print(f"got {len(fds)} FD(s): {fds}")
        for fd in fds:
            try:
                c = read_fd(fd, a.read_chunk)
                print(f"\n--- fd {fd} ({len(c)} bytes) ---\n{c.decode(errors='replace')}")
            except OSError as e:
                print(f"ERR read fd {fd}: {e}", file=sys.stderr)
            finally:
                try: os.close(fd)
                except OSError: pass
        return 0
    finally:
        s.close()
 
 
def pick(socks):
    print(f"\nreadable: {sum(s['r'] for s in socks)}  writable: {sum(s['w'] for s in socks)}  total: {len(socks)}\n")
    for i, s in enumerate(socks):
        fl = ("r" if s["r"] else "-") + ("w" if s["w"] else "-")
        print(f"[{i:>3}] {fl}  {s['path']}  [{LABEL.get(s['type'], '?')}]")
    if not socks:
        return None
    while True:
        try:
            raw = input("\npick number (q to quit): ").strip()
        except EOFError:
            return None
        if raw.lower() in ("q", "quit", "exit"):
            return None
        if raw.isdigit() and 0 <= int(raw) < len(socks):
            return socks[int(raw)]
        print("  invalid")
 
 
def main(a):
    if a.socket_path:
        return read_socket(a.socket_path, a)
    socks = discover(a.search_path or SCAN, a.include_default)
    chosen = pick(socks)
    if a.list_only or chosen is None:
        return 0
    if not chosen["w"]:
        print("[!] no write perm; connect will likely fail")
    return read_socket(chosen["path"], a, chosen["type"])
 
 
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Discover Unix sockets and read one (incl. SCM_RIGHTS FDs).")
    p.add_argument("socket_path", nargs="?", help="connect directly; omit to scan+pick")
    p.add_argument("--search-path", action="append", metavar="DIR", help=f"scan dir (repeatable); default: {' '.join(SCAN)}")
    p.add_argument("--include-default", action="store_true", help="also show systemd/dbus/udev/etc sockets")
    p.add_argument("--list-only", action="store_true", help="list only, don't connect")
    p.add_argument("--timeout", type=float, default=3.0)
    p.add_argument("--max-fds", type=int, default=64)
    p.add_argument("--msg-bufsize", type=int, default=4096)
    p.add_argument("--read-chunk", type=int, default=65536)
    return p.parse_args(argv)
 
 
if __name__ == "__main__":
    sys.exit(main(parse_args()))
