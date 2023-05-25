# Albatross

A [microtransat](https://www.microtransat.org/) attempt.

Probably will use [Icarous](https://github.com/nasa/icarous/tree/master) later on.

## TODO

- Fix fping module in MAVProxy (it only finds IPs on first interface from ifconfig. e.g., misses wlan0)
- Import weirdness in src/camera/base.py

## Setup 

Follow https://www.hackster.io/Matchstic/connecting-pixhawk-to-raspberry-pi-and-nvidia-jetson-b263a7 to setup PixHawk comms

(Mainly for my own info right now)

```bash
python3.9 -m pip install dronekit dronekit-sitl pymavlink

cd ~
git clone https://github.com/Matchstic/albatross.git
mkdir albatross/timelapse
mkdir albatross/logs
cd albatross

# Sort out MAVproxy (Matchstic fork) if needed
sudo apt install fping
sudo cp mavproxy.service /lib/systemd/system/
sudo systemctl enable mavproxy.service

# Assuming you're on a Pi. Update service file if needed.
sudo cp albatross.service /lib/systemd/system/
sudo systemctl enable albatross.service
```

If you want to send telemetry via 4G over VPN (Huawei 3372 4G dongle):

```bash
# https://askubuntu.com/a/1336251
sudo touch /etc/udev/rules.d/41-huawei_e3372.rules
sudo echo "ATTR{idVendor}==\"12d1\", ATTR{idProduct}==\"14dc\", RUN+=\"usb_modeswitch '/%k'\"" >> /etc/udev/rules.d/41-huawei_e3372.rules

sudo apt install openvpn

# Download your .ovpn file from VPN provider
# Make sure the `remote` field is correct

# Assuming you're on a Pi. Update service file if needed.
# This will start OpenVPN if needed
sudo cp 4gvpn.service /lib/systemd/system/
sudo systemctl enable 4gvpn.service
```

## License

Not licensed for use.