# Albatross

A [microtransat](https://www.microtransat.org/) attempt.

Probably will use [Icarous](https://github.com/nasa/icarous/tree/master) later on.

## Setup 

Follow https://www.hackster.io/Matchstic/connecting-pixhawk-to-raspberry-pi-and-nvidia-jetson-b263a7 to setup PixHawk comms

```bash
python3.9 -m pip install dronekit dronekit-sitl pymavlink

# Sort out MAVproxy (Matchstic fork) if needed
sudo cp mavproxy.service /lib/systemd/system/
sudo systemctl enable mavproxy.service

# Assuming you're on a Pi. Change if needed.
sudo cp albatross.service /lib/systemd/system/
sudo systemctl enable albatross.service
```

If you want to send telemetry via 4G over VPN (Huawei 3372 4G dongle):

```bash
# https://askubuntu.com/a/1336251
sudo touch /etc/udev/rules.d/41-huawei_e3372.rules
sudo echo "ATTR{idVendor}==\"12d1\", ATTR{idProduct}==\"14dc\", RUN+=\"usb_modeswitch '/%k'\"" >> /etc/udev/rules.d/41-huawei_e3372.rules

sudo apt install openvpn
```

## License

Not licensed for use.