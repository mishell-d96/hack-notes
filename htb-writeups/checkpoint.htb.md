# checkpoint.htb

## checkpoint.htb

> **OS:** Windows\
> **Difficulty:** Medium\
> **IP:** `10.10.x.x` \
> **Date:** 24-06-2026

As is common in real life pentests, you will start the Checkpoint box with credentials for the following account `alex.turner` / `Checkpoint2024!`

***

### TL;DR

From the account alex.turner it is possible to restore deleted AD object, this returns us the user mark.davies. mark.davies also uses the same password as alex. After that, mark can upload a malicious .vsix file, get a shell, then abuse the badsuccessor exploit that creates a DMSA account with the permissions of the account svc\_deploy. This leads to a share with a .vmem file, which can be parsed with the program vmkatz in order to get the administrator hash.

**Chain:** `alex.turner` > `mark.davies`  > `malicious vsix file` > `badsuccessor` >  `retrieve .vmem file` > `parse with VMKATZ & get admin NT hash`

***

### Box Info

|                |                             |
| -------------- | --------------------------- |
| **Name**       | checkpoint.htb              |
| **OS**         | Windows                     |
| **Difficulty** | Medium                      |
| **Release**    | Released on 13th June, 2026 |
| **Key skills** | Windows AD, Kerberos, vsix  |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Nmap 7.99 scan initiated Sat Jun 13 12:27:19 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN /opt/_NOTES/results/checkpoint/checkpoint.htb/scans/_full_tcp_nmap.txt -oX /opt/_NOTES/results/checkpoint/checkpoint.htb/scans/xml/_full_tcp_nmap.xml checkpoint.htb
Nmap scan report for checkpoint.htb (10.129.15.77)
Host is up, received user-set (0.029s latency).
rDNS record for 10.129.15.77: DC01.checkpoint.htb
Scanned at 2026-06-13 12:27:19 CEST for 202s
Not shown: 65514 filtered tcp ports (no-response)
PORT      STATE SERVICE       REASON          VERSION
53/tcp    open  domain        syn-ack ttl 127 Simple DNS Plus
88/tcp    open  kerberos-sec  syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2026-06-14 16:57:23Z)
135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp   open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: checkpoint.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds? syn-ack ttl 127
464/tcp   open  kpasswd5?     syn-ack ttl 127
593/tcp   open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped    syn-ack ttl 127
3268/tcp  open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: checkpoint.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped    syn-ack ttl 127
5985/tcp  open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        syn-ack ttl 127 .NET Message Framing
49664/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49668/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49673/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49674/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
49683/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49704/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
49712/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2022|2012|2016 (88%)
OS CPE: cpe:/o:microsoft:windows_server_2022 cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_server_2016
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
Aggressive OS guesses: Microsoft Windows Server 2022 (88%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows Server 2016 (85%)
No exact OS matches for host (test conditions non-ideal).
TCP/IP fingerprint:
SCAN(V=7.99%E=4%D=6/13%OT=53%CT=%CU=%PV=Y%DS=2%DC=T%G=N%TM=6A2D3151%P=aarch64-unknown-linux-gnu)
SEQ(SP=106%GCD=2%ISR=109%TI=I%II=I%SS=S%TS=A)
SEQ(SP=107%GCD=1%ISR=103%TI=I%II=I%SS=S%TS=A)
OPS(O1=M552NW8ST11%O2=M552NW8ST11%O3=M552NW8NNT11%O4=M552NW8ST11%O5=M552NW8ST11%O6=M552ST11)
WIN(W1=FFFF%W2=FFFF%W3=FFFF%W4=FFFF%W5=FFFF%W6=FFFF)
ECN(R=Y%DF=Y%TG=80%W=FFFF%O=M552NW8NNS%CC=Y%Q=)
T1(R=Y%DF=Y%TG=80%S=O%A=S+%F=AS%RD=0%Q=)
T2(R=N)
T3(R=N)
T4(R=N)
U1(R=N)
IE(R=Y%DFI=N%TG=80%CD=Z)

Uptime guess: 0.006 days (since Sat Jun 13 12:22:22 2026)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=262 (Good luck!)
IP ID Sequence Generation: Incremental
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2026-06-14T16:58:28
|_  start_date: N/A
|_clock-skew: 1d06h28m23s
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 58029/tcp): CLEAN (Timeout)
|   Check 2 (port 17994/tcp): CLEAN (Timeout)
|   Check 3 (port 61807/udp): CLEAN (Timeout)
|   Check 4 (port 4165/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled and required

TRACEROUTE (using port 139/tcp)
HOP RTT      ADDRESS
1   28.80 ms 10.10.14.1
2   29.27 ms DC01.checkpoint.htb (10.129.15.77)

Read data files from: /usr/share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Jun 13 12:30:41 2026 -- 1 IP address (1 host up) scanned in 202.20 seconds
```

#### 1.2 Initial observations

* Hostname / domain: dc01.checkpoint.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x   DC01.checkpoint.htb checkpoint.htb DC01
    ```

***

### 2. Foothold / Initial Access

#### Description

Explain _why_ this vector works (vulnerability, misconfiguration, CVE number).

#### Exploitation

```bash
# Concrete steps / payload
```

**Result:**

```
# Proof of shell / access
id    # or: whoami
```

> 🚩 **User flag:** `cat user.txt` → `<hash>`

***

### 3. Privilege Escalation / Lateral Movement

#### 3.1 Enumeration as \<user>

```bash
# Linux: linpeas / sudo -l / SUID
# Windows: winpeas / whoami /priv / BloodHound paths
```

**Attack vector:** \<e.g. BadSuccessor / dMSA, Kerberoasting, ADCS ESC1, SUID binary, scheduled task>

#### 3.2 Exploitation

```bash
# Steps
```

**Result:**

```
# Proof of elevated privileges
```

> 🚩 **Root/System flag:** `<hash>`

***

### 4. Post-Exploitation (optional)

* Persistence / dumping secrets (`secretsdump.py`, `lsass`)
* Key loot for the report
* Cleanup notes

***

### 5. Mitigation & Lessons Learned

Short, defensive wrap-up — useful if you ever want to convert this into pentest-report style.

* **Vulnerability:** \<what went wrong>
* **Recommendation:** \<patch / configuration / hardening>
* **What I learned:** \<technique / tool / rabbit hole avoided>

***

### Appendix

#### Tools used

`nmap` · `nxc` · `BloodHound` · `Certipy` · `Impacket` · `<...>`

#### References

* \<link to HackTricks / CVE / blog post>
* <...>
