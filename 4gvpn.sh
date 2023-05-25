#!/bin/bash

# Switches networking to VPN via the Huawei E3372 if no networking is available on wlan0
sleep 10

curl -Is --interface wlan0 http://www.google.com | head -1 | grep 200    

if [[ $? -eq 0 ]]; then   
    echo "Not doing anything, stopping here"
else 
    echo "Starting VPN on 4G dongle"

    # Note: eth0 (wireless dongle) should be the only interface up at this time,
    # therefore all traffic is routed via that.
    openvpn --config /home/pi/client.ovpn
fi