---
layout: post
title: Adblocking
tags: [software, privacy, tutorial]
---

## Prerequisites

1. A Raspberry Pi
2. An micro/SD card reader
3. Admin access to router

## Steps

1. Download and install the [Raspberry Pi Imager](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
2. Insert the SD card into your computer
3. Run the imager
4. Select the OS and SD card in the Imager, and Run. I chose Raspbian Lite because I didn't need Desktop as I would only be running webapps.
![raspberry pi imager](/assets/rpi-imager.gif)
5. After the image has been written to the SD card, create a new file `ssh` on the `boot` volume: `touch ssh`. This allows it to start with SSH enabled, for headless setup. Additional instructions [here](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) for WiFi setup, if you can't connect the Pi via Ethernet.
6. Connect the Pi to power and your local network.
7. Find the Pi's IP address using a tool like [Fing](https://www.fing.com/), your router's DHCP page, or `arp -a` - look for `raspberrypi`.
8. SSH to the Pi: `ssh pi@<IP address>`. It's a new host, so respond *yes* to `Are you sure you want to continue connecting?`. The default password is `raspberry`.
9. Change the password as instructed using `passwd`
10. Install Pi-Hole
```
wget -O basic-install.sh https://install.pi-hole.net
```
11. Note down the admin console password at the end.
12. Log in to the Pi-Hole interface at `<IP address>/admin` and change the password.
11. Configure your DNS following [these instructions](wget -O basic-install.sh https://install.pi-hole.net). I tried to [configure my router](https://discourse.pi-hole.net/t/how-do-i-configure-my-devices-to-use-pi-hole-as-their-dns-server/245) but it didn't work so had to [use the Pi-Hole as my DHCP server](https://discourse.pi-hole.net/t/how-do-i-use-pi-holes-built-in-dhcp-server-and-why-would-i-want-to/3026).
12. Refresh all the DHCP leases on your network - I did this by restarting my router.
13. Log in to the Pi-Hole Admin interface
14. Check the `Settings > DHCP` to verify your devices are using it as the DHCP server.
14. Check the `Network` to verify your devices are using it as the DNS server.
15. Enjoy network-wide ad blocking!
![Pi-Hole Admin Interface](/assets/pi-hole-admin.png)

## Troubleshooting

### I can't access the admin interface at pi.hole 
Restarting the router worked for me.

### I'm loading pages on my device but the Pi-Hole logs don't show the queries
Check if you have any browser extensions or locally running software that is blocking domains. I have a [pretty extensive `/etc/hosts` file](https://github.com/StevenBlack/hosts)[^1] that blocks lots of domains so only domains that aren't blocked at my laptop's network level will make it to the Pi-Hole. 

Footnotes:

[^1]: This is made redundant due to the Pi-Hole also using the same blocklist, but I keep it for when I'm not on my local network.