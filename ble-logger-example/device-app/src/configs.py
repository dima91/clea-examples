import configparser
import os
from pathlib import Path

_FILENAME = os.path.join(str(Path(__file__).parent.parent.absolute()), "config.ini")


def get():
    cfg = configparser.ConfigParser()
    loaded_configs = cfg.read(_FILENAME)
    if not loaded_configs:
        cfg["DEFAULT"] = {
            "wait_time_seconds": 0,
            "discovery_time_sec": 2,
            "interaction_min_time_sec": 20,
            "interaction_min_rssi": -70,
        }
        device_id, realm, credential_secret, pairing_base_url = setup_dialog()
        cfg["ASTARTE"] = {
            "device_id": device_id,
            "realm": realm,
            "credentials_secret": credential_secret,
            "pairing_base_url": pairing_base_url,
        }
        with open(_FILENAME, "w") as configfile:
            cfg.write(configfile)
    config_object = {
        "wait_time_seconds": int(cfg["DEFAULT"]["wait_time_seconds"]),
        "discovery_time_sec": int(cfg["DEFAULT"]["discovery_time_sec"]),
        "interaction_min_time_sec": int(cfg["DEFAULT"]["interaction_min_time_sec"]),
        "interaction_min_rssi": int(cfg["DEFAULT"]["interaction_min_rssi"]),
        "device_id": cfg["ASTARTE"]["device_id"],
        "realm": cfg["ASTARTE"]["realm"],
        "credentials_secret": cfg["ASTARTE"]["credentials_secret"],
        "pairing_base_url": cfg["ASTARTE"]["pairing_base_url"],
    }
    return config_object


def setup_astarte():
    cfg = configparser.ConfigParser()
    loaded_configs = cfg.read(_FILENAME)
    if not loaded_configs:
        cfg["DEFAULT"] = {
            "wait_time_seconds": 0,
            "discovery_time_sec": 2,
            "interaction_min_time_sec": 20,
            "interaction_min_rssi": -70,
        }
    device_id, realm, credential_secret, pairing_base_url = setup_dialog()
    cfg["ASTARTE"] = {
        "device_id": device_id,
        "realm": realm,
        "credentials_secret": credential_secret,
        "pairing_base_url": pairing_base_url,
    }
    with open(_FILENAME, "w") as configfile:
        cfg.write(configfile)


def setup_dialog():
    print("Configure Astarte device")
    device_id = input("device id: ")
    print("-> {}".format(device_id))
    realm = input("realm: ")
    print("-> {}".format(realm))
    credential_secret = input("credential secret: ")
    print("-> {}".format(credential_secret))
    pairing_base_url = input("pairing base url (without api version): ")
    if pairing_base_url[-1] == "/":
        pairing_base_url = pairing_base_url[0:-1]
    print("-> {}".format(pairing_base_url))
    return device_id, realm, credential_secret, pairing_base_url
