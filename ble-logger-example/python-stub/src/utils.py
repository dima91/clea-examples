
import random
from enum import Enum


class DeviceType(Enum): 
    ACCESSORY   = 0
    SMARTPHONE  = 1


def generate_mac_address() -> str:
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),\
                                                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def build_weighted_list(target_map) -> list:
    # Checking also that  weights summation is equal to one
    tmp_sum = 0.0
    result  = []
    
    for k in target_map:
        tmp_sum += target_map[k]
        if len(result)==0:
            result.append({"id":k, "lower_bound":target_map[k]})
        else:
            last    = result[-1]
            result.append({"id":k, "lower_bound":target_map[k]+last["lower_bound"]})
    
    if tmp_sum != 100:
        print(f"Items weitghts summation differs from 100 -> {tmp_sum}")
        raise Exception
    
    return result