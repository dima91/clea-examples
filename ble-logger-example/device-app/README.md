# BLE Scanner App
## Usage
`python3 ./scan.py`

## Help
```
> python3 scan.py --help
usage: scan [-h] [-v] [-c]

BLE Scanner

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -c, --config   Configure Astarte
```

## Install

You can also install the script as a Linux daemon in order to starting it with `systemd`.
To do so, use `install.sh` script: it will install the dependencies, will invoke the `scan.py` script to configure the environment and will install the `ble-scanner.service` file so that it can be executed automatically when system boot.