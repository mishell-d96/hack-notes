# 113 - IDENT

* [ ] 1\. **general checks ident**

```bash
##### REFERENCE: https://blog.1nf1n1ty.team/hacktricks/network-services-pentesting/113-pentesting-ident
# ---
# DESCRIPTION:
# ---
# What's Happening when the IDENT service is running

# 1. Port 113 (ident service) is open and responding
# 2. When nmap's -sC flag runs its default NSE scripts, it includes the auth-owners script
# 3. This script queries the ident service on port 113, asking: "Which user owns the process listening on port X?"
# 4. The ident service responds with the username for each port

# 1. use nmap to check for ident service
nmap -sC {{RHOST}}

# example output
Starting Nmap 7.98 ( https://nmap.org ) at 2026-01-28 11:55 +0100
Nmap scan report for 192.168.204.60
Host is up (0.021s latency).
Not shown: 994 filtered tcp ports (no-response)
PORT      STATE  SERVICE
22/tcp    open   ssh
|_auth-owners: root # USER root on system
| ssh-hostkey: 
|   2048 75:...
113/tcp   open   ident
|_auth-owners: nobody # USER nobody on system
8080/tcp  open   http-proxy
|_http-title: Redmine
| http-robots.txt: 10 disallowed entries 
| /projects/test/....
10000/tcp open   snet-sensor-mgmt
|_auth-owners: eleanor # USER eleanor on system

# 2. if there is a SSH server, try connecting with the identified users
# bruteforce with hydra 'SSH'

```
