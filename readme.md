# Albatross

A [microtransat](https://www.microtransat.org/) attempt.

Probably will use [Icarous](https://github.com/nasa/icarous/tree/master) later on.

## Setup 

Follow https://www.hackster.io/Matchstic/connecting-pixhawk-to-raspberry-pi-and-nvidia-jetson-b263a7 to setup PixHawk comms

```bash
python3.9 -m pip install dronekit dronekit-sitl pymavlink

# Assuming you're on a Pi. Change if needed.
sudo cp albatross.service /lib/systemd/system/
sudo systemctl enable albatross.service
```

## License

Not licensed for use.