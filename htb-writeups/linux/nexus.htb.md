# nexus.htb

> **OS:** Linux
>
> **Difficulty:** Easy
>
> **IP:** `10.10.x.x`
>
> **Date:** 03-07-2026

​

***

### TL;DR <a href="#tl-dr" id="tl-dr"></a>

<...>

**Chain:**&#x200B;

***

### Box Info <a href="#box-info" id="box-info"></a>

| **Name**       | nexus.htb                   |
| -------------- | --------------------------- |
| **OS**         | Linux                       |
| **Difficulty** | Easy                        |
| **Release**    | Released on 23th June, 2026 |
| **Key skills** |                             |

​

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

After some research, we find a .env file with another password within the krayin folder `/var/www/krayin` and abuse this in order to login as the user `jones` :&#x20;

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.16.15.png" alt=""><figcaption></figcaption></figure>

We can then login to the app with the combination: `jones:y27xb3ha!!74GbR`&#x20;

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-07-18 om 14.18.18.png" alt=""><figcaption></figcaption></figure>

***

### 3. Privilege Escalation <a href="#id-3.-privilege-escalation" id="id-3.-privilege-escalation"></a>

**3.1 Description**

> ​

​
