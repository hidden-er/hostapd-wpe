#!/bin/bash

export PATH="/usr/local/bin:/usr/bin:/bin"
exec 2> /var/log/hostapd-wpe-error.log

systemctl stop NetworkManager
ifconfig wlan0 down
ifconfig wlan0 up
airmon-ng check kill
hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf