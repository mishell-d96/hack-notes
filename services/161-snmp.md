# 161 - SNMP

* [ ] 1\. **general checks SNMP**

```bash
##### REFERENCE: https://hackviser.com/tactics/pentesting/services/snmp
# 1. read the 'public' community string from a target host               
snmpwalk -v1 -c public {{RHOST}}

# 2. read the 'public' community string from a target host where hex output is converted to ASCII (suggested)
snmpwalk -v2c -c public {{RHOST}} -Oa

##### most common 'community strings' that can be utilized by snmpwalk
public
private
manager
security

##### versions utilized by snmp
v1
v2
v2c
v3

# 3. check the nsExtendObjects
snmpwalk -v 2c -c public {{RHOST}} nsExtendObjects

### ---
# snmp-check
### ---

# 1. basic usage snmp-check
snmp-check -t {{RHOST}} -c public

# 2. if community string is unknown, it might try default ones like 'public'
snmp-check -t {{RHOST}}

# search for:
# - user accounts/ passwords
# - software (versions)
# - network configuration
```
