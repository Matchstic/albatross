#!/bin/bash

# Switches networking to VPN via the Huawei E3372 if no networking is available
sleep 10

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Not doing anything, stopping here"
else
    echo "Starting VPN on 4G dongle"
    openvpn --config /home/pi/client.ovpn
fi
