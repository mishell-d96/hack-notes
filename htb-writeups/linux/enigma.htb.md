# enigma.htb

> **OS:** Linux\
> **Difficulty:** Easy\
> **IP:** `10.10.x.x`\
> **Date:** 03-07-2026

***

### TL;DR

While enumerating the NFS share, we discovered a `.pdf` file containing credentials for the user **kevin** on the subdomain `mail001.enigma.htb`, which hosts Roundcube. After logging in, we found an email from Sarah in kevin's inbox. We then reused kevin's credentials to authenticate as the user **sarah**, whose mailbox contained a second set of credentials — this time for the **admin** account on the **OpenSTAManager** application.

After identifying the software version, we determined it was vulnerable to both command injection and SQL injection. Exploiting these gave us a shell as **www-data** and yielded credentials for the user **haris**. From the www-data shell, we escalated to **haris**, and eventually identified an application listening on `127.0.0.1:1337` that was vulnerable to code execution. Exploiting this granted us a **root** shell.

**Chain:**

`nfs` > `roundcube` (mail001.enigma.htb) > `OpenSTAManager` (support\_001.enigma.htb) > `www-data` > `sudo to haris` > `olivetin` > `root`

***

### Box Info

|                |                                                        |
| -------------- | ------------------------------------------------------ |
| **Name**       | enigma.htb                                             |
| **OS**         | Linux                                                  |
| **Difficulty** | Easy                                                   |
| **Release**    | Released on 27th June, 2026                            |
| **Key skills** | NFS, SQL injection, Command injection, public exploits |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Nmap 7.99 scan initiated Fri Jul  3 10:59:17 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN /opt/_NOTES/results/enigma/enigma.htb/scans/_full_tcp_nmap.txt -oX /opt/_NOTES/results/enigma/enigma.htb/scans/xml/_full_tcp_nmap.xml enigma.htb
Nmap scan report for enigma.htb (10.129.28.177)
Host is up, received user-set (0.10s latency).
rDNS record for 10.129.28.177: enigma
Scanned at 2026-07-03 10:59:17 CEST for 806s
Not shown: 65522 closed tcp ports (reset)
PORT      STATE SERVICE  REASON         VERSION
22/tcp    open  ssh      syn-ack ttl 63 OpenSSH 9.6p1 Ubuntu 3ubuntu13.16 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0c:4b:d2:76:ab:10:06:92:05:dc:f7:55:94:7f:18:df (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBN9Ju3bTZsFozwXY1B2KIlEY4BA+RcNM57w4C5EjOw1QegUUyCJoO4TVOKfzy/9kd3WrPEj/FYKT2agja9/PM44=
|   256 2d:6d:4a:4c:ee:2e:11:b6:c8:90:e6:83:e9:df:38:b0 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH9qI0OvMyp03dAGXR0UPdxw7hjSwMR773Yb9Sne+7vD
80/tcp    open  http     syn-ack ttl 63 nginx 1.24.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.24.0 (Ubuntu)
|_http-title: Enigma Corp \xE2\x80\x94 Managed IT Solutions
110/tcp   open  pop3     syn-ack ttl 63 Dovecot pop3d
|_pop3-capabilities: STLS SASL RESP-CODES UIDL PIPELINING TOP AUTH-RESP-CODE CAPA
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=enigma
| Subject Alternative Name: DNS:enigma
| Issuer: commonName=enigma
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-02-18T20:33:33
| Not valid after:  2036-02-16T20:33:33
| MD5:     8361 ca20 2e4e dff6 6e90 1445 7458 9fc3
| SHA-1:   9f91 b6ed 85b4 517c 0421 c62e 167d 5631 daa6 5a40
| SHA-256: 98a8 1f62 b59c 832a 162e 2394 9e41 1e08 46a0 f7c1 529f afcb ea15 eea5 ef52 bb70
| -----BEGIN CERTIFICATE-----
<...>
|_-----END CERTIFICATE-----
111/tcp   open  rpcbind  syn-ack ttl 63 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      34302/udp6  mountd
|   100005  1,2,3      36903/tcp6  mountd
|   100005  1,2,3      41191/udp   mountd
|   100005  1,2,3      57773/tcp   mountd
|   100021  1,3,4      37265/tcp   nlockmgr
|   100021  1,3,4      38189/tcp6  nlockmgr
|   100021  1,3,4      51529/udp   nlockmgr
|   100021  1,3,4      60314/udp6  nlockmgr
|   100024  1          37647/tcp6  status
|   100024  1          42567/udp   status
|   100024  1          50950/udp6  status
|   100024  1          52069/tcp   status
|   100227  3           2049/tcp   nfs_acl
|_  100227  3           2049/tcp6  nfs_acl
143/tcp   open  imap     syn-ack ttl 63 Dovecot imapd (Ubuntu)
|_ssl-date: TLS randomness does not represent time
|_imap-capabilities: have STARTTLS LOGIN-REFERRALS more ID post-login IMAP4rev1 Pre-login LITERAL+ ENABLE SASL-IR OK IDLE LOGINDISABLEDA0001 capabilities listed
| ssl-cert: Subject: commonName=enigma
| Subject Alternative Name: DNS:enigma
| Issuer: commonName=enigma
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-02-18T20:33:33
| Not valid after:  2036-02-16T20:33:33
| MD5:     8361 ca20 2e4e dff6 6e90 1445 7458 9fc3
| SHA-1:   9f91 b6ed 85b4 517c 0421 c62e 167d 5631 daa6 5a40
| SHA-256: 98a8 1f62 b59c 832a 162e 2394 9e41 1e08 46a0 f7c1 529f afcb ea15 eea5 ef52 bb70
| -----BEGIN CERTIFICATE-----
<...>
|_-----END CERTIFICATE-----
993/tcp   open  ssl/imap syn-ack ttl 63 Dovecot imapd (Ubuntu)
|_imap-capabilities: have LOGIN-REFERRALS more ID post-login SASL-IR AUTH=PLAINA0001 LITERAL+ ENABLE IMAP4rev1 Pre-login IDLE OK capabilities listed
| ssl-cert: Subject: commonName=enigma
| Subject Alternative Name: DNS:enigma
| Issuer: commonName=enigma
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-02-18T20:33:33
| Not valid after:  2036-02-16T20:33:33
| MD5:     8361 ca20 2e4e dff6 6e90 1445 7458 9fc3
| SHA-1:   9f91 b6ed 85b4 517c 0421 c62e 167d 5631 daa6 5a40
| SHA-256: 98a8 1f62 b59c 832a 162e 2394 9e41 1e08 46a0 f7c1 529f afcb ea15 eea5 ef52 bb70
| -----BEGIN CERTIFICATE-----
<...>
|_-----END CERTIFICATE-----
|_ssl-date: TLS randomness does not represent time
995/tcp   open  ssl/pop3 syn-ack ttl 63 Dovecot pop3d
|_pop3-capabilities: USER SASL(PLAIN) RESP-CODES UIDL PIPELINING TOP AUTH-RESP-CODE CAPA
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=enigma
| Subject Alternative Name: DNS:enigma
| Issuer: commonName=enigma
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-02-18T20:33:33
| Not valid after:  2036-02-16T20:33:33
| MD5:     8361 ca20 2e4e dff6 6e90 1445 7458 9fc3
| SHA-1:   9f91 b6ed 85b4 517c 0421 c62e 167d 5631 daa6 5a40
| SHA-256: 98a8 1f62 b59c 832a 162e 2394 9e41 1e08 46a0 f7c1 529f afcb ea15 eea5 ef52 bb70
| -----BEGIN CERTIFICATE-----
<...>
|_-----END CERTIFICATE-----
2049/tcp  open  nfs_acl  syn-ack ttl 63 3 (RPC #100227)
37265/tcp open  nlockmgr syn-ack ttl 63 1-4 (RPC #100021)
37499/tcp open  mountd   syn-ack ttl 63 1-3 (RPC #100005)
52069/tcp open  status   syn-ack ttl 63 1 (RPC #100024)
57773/tcp open  mountd   syn-ack ttl 63 1-3 (RPC #100005)
58811/tcp open  mountd   syn-ack ttl 63 1-3 (RPC #100005)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
TCP/IP fingerprint:
OS:SCAN(V=7.99%E=4%D=7/3%OT=22%CT=1%CU=36265%PV=Y%DS=2%DC=T%G=Y%TM=6A477D0B
OS:%P=aarch64-unknown-linux-gnu)SEQ(SP=100%GCD=1%ISR=106%TI=Z%CI=Z%TS=A)OPS
OS:(O1=M552ST11NW7%O2=M552ST11NW7%O3=M552NNT11NW7%O4=M552ST11NW7%O5=M552ST1
OS:1NW7%O6=M552ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)ECN
OS:(R=Y%DF=Y%T=40%W=FAF0%O=M552NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Uptime guess: 2.743 days (since Tue Jun 30 17:23:28 2026)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=256 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 1723/tcp)
HOP RTT      ADDRESS
1   94.45 ms 10.10.14.1
2   94.53 ms enigma (10.129.28.177)

Read data files from: /usr/share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Jul  3 11:12:43 2026 -- 1 IP address (1 host up) scanned in 806.26 seconds

```

#### 1.2 Initial observations

* Hostname / domain: enigma.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x enigma.htb 
    ```

#### 1.3 Enumerate NFS exports with showmount

Run `showmount -e enigma.htb` to list the NFS exports available from the target. The output shows that `/srv/nfs/onboarding` is exposed and can be mounted locally.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-06 om 15.39.43.png" alt=""><figcaption></figcaption></figure>

After that, mount the NFS export to the local `mount` folder with the following command

```bash
mount -t nfs enigma.htb:/srv/nfs/onboarding mount -o nolock
```

And notice that there is an `New_Employee_Access.pdf` file.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-06 om 15.43.04.png" alt=""><figcaption></figcaption></figure>

The contents of the .pdf file are as follows:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-06 om 15.44.51.png" alt=""><figcaption></figcaption></figure>

We then add the `mail001.enigma.htb` record to the /etc/hosts file, and continue navigating to the roundcube webapp.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-06 om 15.46.58.png" alt=""><figcaption></figcaption></figure>

Inside Roundcube, we find an email from `sarah` to Kevin. We later confirm that the password `Enigma2024!` also works for e-mail account `sarah`. After logging in as Sarah, we find the following credentials about OpenSTAManager with admin credentials.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-06 om 15.56.55.png" alt=""><figcaption></figcaption></figure>

After seeing the mail sarah recieved from IT, I updated the `/etc/hosts` file. The file is now as follows:

```bash
# HTB
10.129.30.247 enigma enigma.htb mail001.enigma.htb support_001.enigma.htb
```

The admin credentials work on openSTAManager, and we notice that the version 2.9.8 contains 2 vulnerabilities; 1: an SQL injection, from which we retrieve the bcrypt hash of the user&#x20;



### 2. Foothold / Initial Access

#### 2.1 Description

<...>

#### 2.2 Exploitation

***

### 3. Privilege Escalation

#### 3.1 Description

<...>

```
```
