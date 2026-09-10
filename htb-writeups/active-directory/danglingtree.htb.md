# danglingtree.htb

> **OS:** Windows\
> **Difficulty:** Medium\
> **IP:** `10.10.x.x`\
> **Date:** 03-07-2026

***

### TL;DR

<...>

**Chain:**&#x20;

***

### Box Info

|                |                              |
| -------------- | ---------------------------- |
| **Name**       | danglingtree.htb             |
| **OS**         | Windows                      |
| **Difficulty** | Medium                       |
| **Release**    | Released on 8th August, 2026 |
| **Key skills** |                              |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Nmap 7.99 scan initiated Wed Sep  2 02:24:34 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -p- -oN /opt/_NOTES/results/danglingtree/danglingtree.htb/scans/_full_tcp_nmap.txt -oX /opt/_NOTES/results/danglingtree/danglingtree.htb/scans/xml/_full_tcp_nmap.xml danglingtree.htb
Nmap scan report for danglingtree.htb (10.129.78.88)
Host is up, received user-set (0.094s latency).
rDNS record for 10.129.78.88: DC.danglingtree.htb
Scanned at 2026-09-02 02:24:34 CEST for 636s
Not shown: 65510 filtered tcp ports (no-response)
PORT      STATE SERVICE            REASON          VERSION
53/tcp    open  domain             syn-ack ttl 127 Simple DNS Plus
80/tcp    open  http               syn-ack ttl 127 Microsoft IIS httpd 10.0
88/tcp    open  kerberos-sec       syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2026-09-03 20:33:15Z)
135/tcp   open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn        syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp   open  ldap               syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: danglingtree.htb, Site: Default-First-Site-Name)
443/tcp   open  ssl/https?         syn-ack ttl 127
| tls-alpn: 
|   h2
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=danglingtree-DC-CA/domainComponent=danglingtree
| Issuer: commonName=danglingtree-DC-CA/domainComponent=danglingtree
| Public Key type: rsa
| Public Key bits: 4096
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2026-03-26T05:34:19
| Not valid after:  2114-03-26T05:44:18
| MD5:     9054 595f c5e0 bb67 628f f4fc 8d82 a8cf
| SHA-1:   9733 440c 1fd9 f7c9 db9e d4e8 69b7 7b8e 8e71 7781
| SHA-256: fb01 7a29 c4a9 3bee db84 2c1d 77e4 6cd3 d00b 89d8 8229 a712 c4ca db44 3678 29a0
| -----BEGIN CERTIFICATE-----
<...>
|_-----END CERTIFICATE-----
445/tcp   open  microsoft-ds?      syn-ack ttl 127
464/tcp   open  kpasswd5?          syn-ack ttl 127
593/tcp   open  ncacn_http         syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap           syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: danglingtree.htb, Site: Default-First-Site-Name)
3268/tcp  open  ldap               syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: danglingtree.htb, Site: Default-First-Site-Name)
3269/tcp  open  ssl/ldap           syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: danglingtree.htb, Site: Default-First-Site-Name)
3389/tcp  open  ssl/ms-wbt-server? syn-ack ttl 127
6600/tcp  open  ssl/mshvlm?        syn-ack ttl 127
9389/tcp  open  mc-nmf             syn-ack ttl 127 .NET Message Framing
49664/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49677/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49679/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49682/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49684/tcp open  ncacn_http         syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
49692/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49713/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49725/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC
49759/tcp open  msrpc              syn-ack ttl 127 Microsoft Windows RPC

Read data files from: /usr/share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Sep  2 02:35:10 2026 -- 1 IP address (1 host up) scanned in 636.23 seconds

```

#### 1.2 Initial observations

* Hostname / domain: dc.danglingtree.htb
* Added to `/etc/hosts`:

```
10.129.x.x     DC.danglingtree.htb danglingtree.htb DC 
```

#### 1.3 enumerating shares

After adding the domain controller to `/etc/hosts`  we run an script for enumerating the shares as a guest user. This output returns a .pdf file with credentials associated

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 11.53.17.png" alt=""><figcaption></figcaption></figure>

When opening the .PDF file, we find credentials of the user anderson.w and can continue out pentest to the initial user

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 11.54.46.png" alt=""><figcaption></figcaption></figure>

### 2. Foothold / Initial Access

#### 2.1 Description

> ...

#### 2.2 Exploitation



***

### 3. Privilege Escalation

#### 3.1 Description

>

```
```
