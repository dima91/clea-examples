
import random
from enum import Enum


class DeviceType(Enum): 
    ACCESSORY   = 0
    SMARTPHONE  = 1


def generate_mac_address() -> str:
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),\
                                                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))