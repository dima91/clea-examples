
import asyncio, random
from datetime import datetime, timedelta
from typing import Tuple

import utils


class DeviceGenerator:
    
    __config                = None
    __last_generation_time  = None

    def __init__(self, config) -> None:
        self.__config               = config
        self.__last_generation_time = datetime.now()


    def generate_device(self, curr_devices_count) -> Tuple[str, int]:
        device_addess   = ""
        time            = random.uniform(self.__config["min_presence_time_s"], self.__config["max_presence_time_s"])
        now             = datetime.now()

        if (now-self.__last_generation_time).total_seconds()>self.__config["creation_delay_s"] and \
            random.random()>self.__config["min_creation_probability"] and \
            curr_devices_count<self.__config["max_devices_count"] :
            
            self.__last_generation_time = now
            device_addess               = utils.generate_mac_address()
        
        return device_addess, time




class Simulator:

    __config            = None
    __client            = None
    __generator         = None
    __current_devices   = None

    def __init__(self, config, astarte_client) -> None:
        
        self.__config           = config
        self.__client           = astarte_client
        self.__generator        = DeviceGenerator(self.__config["devices"])
        self.__current_devices  = []


    async def run(self) -> None:
        try:
            print ("Running..")

            while True:
                await asyncio.sleep(5)

                now             = datetime.now()
                expired_devices = []

                # Trying to generate a new device
                device, presence_time   = self.__generator.generate_device(len(self.__current_devices))
                if device!="":
                    print (f"Registering a new device! (Current device count {len(self.__current_devices)})")
                    self.__current_devices.append({
                        "device_address"    : device,
                        "creation_time"     : now,
                        "presence_time"     : presence_time
                    })

                # Removing expired devices
                i   = 0
                while i<len(self.__current_devices):
                    d   = self.__current_devices[i]
                    if (now-d["creation_time"]).total_seconds()>d["presence_time"]:
                        # Removing current device
                        expired_devices.append(self.__current_devices.pop(i))
                    else:
                        i += 1
                
                # Publishing expired device
                self.__client.publish_devices(expired_devices)
                        

        except Exception as e:
            print("Catched following exception!!")
            print(e)