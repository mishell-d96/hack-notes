# 6379 - REDIS

* [ ] **1. general checks VNC** Pentesting VNC

```language-bash
##### REFERENCE: https://www.emmanuelsolis.com/oscp.html
# 1. nmap scan & banner grabbing
nmap -p 5900 --script vnc-info,vnc-auth-bypass {{RHOST}}

# 2. use vncviewer or tigervnc to connect to a VNC server
vncviewer {{RHOST}}:5900

# 3. more detailed connection with authentication
vncviewer -passwd /path/to/passwordfile {{RHOST}}:5900

# common default credentials:
No Password
vnc
1234

```

* [ ] **2. bruteforce VNC** Pentesting VNC

```language-bash
##### REFERENCE: https://www.emmanuelsolis.com/oscp.html
# 1A. username + password combination
# 1B. lowercase usernames + password combination
# 1C. -e snr = try 'blank' passwords, 'n' for username = password, 'r' for reversed username
hydra -L users.txt -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} vnc
hydra -L <(tr A-Z a-z < users.txt) -P /usr/share/wordlists/fasttrack.txt -e nsr {{RHOST}} vnc
```
