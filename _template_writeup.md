# \_TEMPLATE\_writeup

## \<Box Name> — HTB Writeup

> **OS:** \<Linux / Windows>\
> **Difficulty:** \<Easy / Medium / Hard / Insane>\
> **IP:** `10.10.x.x` \
> **Date:** \<YYYY-MM-DD>

***

### TL;DR

Short summary of the full attack chain in 2-4 sentences. Anyone should be able to read the path from `nmap` to `root`/`SYSTEM`/`Domain Admin` at a glance.

**Chain:** `<service/cve>` → `<foothold>` → `<lateral/privesc>` → `<root>`

***

### Box Info

|                |                                        |
| -------------- | -------------------------------------- |
| **Name**       | \<Box Name>                            |
| **OS**         | \<Linux / Windows>                     |
| **Difficulty** | <...>                                  |
| **Release**    | \<date>                                |
| **Key skills** | \<e.g. AD, Kerberos, web exploitation> |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Fast full TCP scan
nmap -p- -sC -sV -sS 10.10.x.x -oN nmap/allports.txt

# Service and version detection on open ports
nmap -p <ports> -sCV 10.10.x.x -oN nmap/services.txt
```

**Open ports:**

```bash
# add open ports


```

#### 1.2 Initial observations

* Hostname / domain: `<domain.local>`
*   Added to `/etc/hosts`:

    ```
    10.10.x.x   <box>.htb dc01.<box>.htb
    ```
* Notable items: <...>

***

### 2. Enumeration

| Credential  | Source    | Works on   |
| ----------- | --------- | ---------- |
| `user:pass` | \<source> | \<service> |
|             |           |            |

***

### 3. Foothold / Initial Access

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

### 4. Privilege Escalation / Lateral Movement

#### 4.1 Enumeration as \<user>

```bash
# Linux: linpeas / sudo -l / SUID
# Windows: winpeas / whoami /priv / BloodHound paths
```

**Attack vector:** \<e.g. BadSuccessor / dMSA, Kerberoasting, ADCS ESC1, SUID binary, scheduled task>

#### 4.2 Exploitation

```bash
# Steps
```

**Result:**

```
# Proof of elevated privileges
```

> 🚩 **Root/System flag:** `<hash>`

***

### 5. Post-Exploitation (optional)

* Persistence / dumping secrets (`secretsdump.py`, `lsass`)
* Key loot for the report
* Cleanup notes

***

### 6. Mitigation & Lessons Learned

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
