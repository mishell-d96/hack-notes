# AS-REP roasting

### AS-REP roasting

AS-REP roasting targets Active Directory accounts that have Kerberos pre-authentication disabled ("Do not require Kerberos preauthentication"). Normally a client must prove knowledge of its password before the KDC responds, but for these accounts an attacker can request an authentication ticket (AS-REP) for the user without any credentials, and the KDC returns a response containing data encrypted with the user's password-derived key. The attacker (typically using Impacket's GetNPUsers or Rubeus) extracts this encrypted blob and cracks it offline with Hashcat to recover the account's plaintext password. The risk is credential theft leading to lateral movement and privilege escalation, especially dangerous if a roastable account is privileged or reuses a weak password, and the root cause is that disabling Kerberos pre-authentication (often set for legacy compatibility) lets anyone request encrypted material tied to a user's password, turning a weak password into an offline-crackable hash without needing any prior access.

<figure><img src="../../.gitbook/assets/afbeelding (5).png" alt=""><figcaption></figcaption></figure>

### Exploitation

```bash
# 1. Retrieve all - AS-REP roastable accounts from the domain in hashcat format (domain users samaccount names in users.txt)
GetNPUsers.py '{{DOMAIN}}'.'{{ROOTDNS}}'/ -usersfile users.txt -format hashcat -outputfile hashes.asreproast
 
# 2. Utilizing nxc
nxc ldap {{RHOST}} -u '{{USERNAME}}' -p '{{PASSWORD}}' --asreproast asreproast.txt
```



