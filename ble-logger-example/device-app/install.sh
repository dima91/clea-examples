
#!/bin/bash

# Installing dependencies
pip3 install -r requirements.txt
# Configuring the enviornment and configuration file
python3 scan.py -c
# Installing the system file
sudo cp ble-scanner.service /etc/systemd/system
# Enabling the execution at start-up
sudo systemctl enable ble-scanner
sudo systemctl daemon-reload
