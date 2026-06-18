# 21 - FTP

* [ ] 1\. **general checks FTP**

```bash
##### REFERENCE:
https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-ftp/index.html?highlight=PENTESTING%20FTP#21---pentesting-ftp                
                
# 1. 'nmap' and 'nc'
nmap -sC -sV -p 21 {{RHOST}} --script=ftp*
nc -vn {{RHOST}} 21

# 2. Check for anonymous login
# anonymous : anonymous
# _anonymous :
# _ftp : ftp

ftp {{RHOST}}
> anonymous
> anonymous
> ls -a # list all files (even hidden)
> binary # set transmission to binary instead of ascii
> ascii # set transmission to ascii instead of binary

# 3. if you can login:
# - Any for sensitive files?
# - Possible webroot directory?
# - Useful paths within files you can access with an other vuln, e.g.: LFI?

# 4. if it is a lot, download all files:
wget -m ftp://anonymous:anonymous@{{RHOST}}
wget -m --no-passive ftp://anonymous:anonymous@{{RHOST}}

```

* [ ] **2. Bruteforce FTP**

```bash
### ---
# NOTE: if there is a website, extract (if applicable) users and passwords. Use that as a base for the wordlists
### ---

# 1. FTP (plaintext)
# 1A. username + password combination
# 1B. lowercase usernames + password combination
# 1C. -e snr = try 'blank' passwords, 'n' for username = password, 'r' for reversed username
hydra -L users.txt -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} ftp
hydra -L <(tr A-Z a-z < users.txt) -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} ftp
```
