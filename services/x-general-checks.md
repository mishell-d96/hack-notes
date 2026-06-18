# X - General checks

### Unknown port (x)

* [ ] **1. general checks unknown ports**

```bash
# 1. 'nmap' and 'nc'
nmap -sC -sV -p x {{RHOST}}
nc -vn {{RHOST}} x

# 2. after connecting with netcat, try common commands like:
help
?
ls
info
```
