
import asyncio, random, holidays, traceback
from datetime import datetime, timedelta
from typing import Tuple

from astarte_client import AstarteClient

import utils
from utils import DeviceType


class DevicesManager:

    __MINUTE_DELAY_S    = 60
    __HOURLY_DELAY_S    = 3600
    __DAILY_DELAY_S     = 86400

    __config            = None
    __holidays          = None
    __nearby_devices    = None

    __minute_devices_cache  = None
    __hourly_devices_cache  = None
    __daily_devices_cache   = None
    
    def __init__(self, config, country) -> None:
        self.__config           = config
        self.__holidays         = holidays.country_holidays(country)
        self.__nearby_devices   = {}

        self.__minute_devices_cache = {}
        self.__hourly_devices_cache = {}
        self.__daily_devices_cache  = {}


    def __update_local_cache(self, cache, address, device) -> None:
        if not (address in cache):
            cache[address]  = device


    def generate_nearby_devices(self, now:datetime) -> None:
        if not (now.date() in self.__holidays):
            
            generation_probability  = self.__config['generation_probabilities'][str(now.hour)]
            new_devices_range       = self.__config['generation_number_ranges'][str(now.hour)]
            presence_time_range     = self.__config['presence_time_ranges_s'][str(now.hour)]

            if random.random() <= generation_probability:
                devices_count   = random.randint(new_devices_range[0], new_devices_range[1])
                print(f"Generating {devices_count} devices @ {now}")
                
                for i in range(devices_count):
                    addr            = utils.generate_mac_address()
                    if not (addr in self.__nearby_devices):
                        device_type                 = DeviceType.SMARTPHONE \
                                                        if random.random()<=self.__config['smartphone_probability'] \
                                                        else DeviceType.ACCESSORY
                        device_vendor_idx           = random.choice(self.__config['admitted_smartphones_vendors']) \
                                                        if device_type==DeviceType.SMARTPHONE \
                                                        else random.choice(self.__config['admitted_accessories_vendors'])
                        self.__nearby_devices[addr] = {
                            "presence_time"     : random.randint(presence_time_range[0], presence_time_range[1]),
                            "creation_time"     : now,
                            "device_type"       : device_type,
                            "device_vendor_idx" : "Unknown" if device_vendor_idx=="-1" else device_vendor_idx
                        }

                        print(f"Generated device: {self.__nearby_devices[addr]}")


    def prune_nearby_devices(self, now:datetime) -> None:
        #print("Pruning nearby devices")
        to_be_popped    = []
        for addr in self.__nearby_devices:
            item    = self.__nearby_devices[addr]
            if (now-item['creation_time']).total_seconds()>item['presence_time']:
                print(f"Adding {addr} in caches")
                to_be_popped.append(addr)
                self.__update_local_cache(self.__minute_devices_cache, addr, item)
                self.__update_local_cache(self.__hourly_devices_cache, addr, item)
                self.__update_local_cache(self.__daily_devices_cache, addr, item)
        for addr in to_be_popped:
            self.__nearby_devices.pop(addr)


    def dump_and_clear_minute_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__MINUTE_DELAY_S:
            # TODO
            pass

        return None
    
    
    def dump_and_clear_hourly_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__HOURLY_DELAY_S:
            # TODO
            pass

        return None
    
    
    def dump_and_clear_daily_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__DAILY_DELAY_S:
            # TODO
            pass

        return None




class Simulator:

    __config            = None
    __client            = None
    __devices_manager   = None

    def __init__(self, config:dict, astarte_client:AstarteClient) -> None:
        
        self.__config           = config
        self.__client           = astarte_client
        self.__devices_manager  = DevicesManager(self.__config['ble_devices'], self.__config['country'])


    async def run(self) -> None:
        try:
            print ("Running Simulator loop..")

            now                     = datetime.now()
            loop_delay              = self.__config["loop_delay_s"]
            last_minute_stats_time  = now.replace(microsecond=0, second=0)
            last_hourly_stats_time  = last_minute_stats_time.replace(minute=0)
            last_daily_stats_time   = last_minute_stats_time.replace(hour=0)

            while True:
                await asyncio.sleep(loop_delay)
                now = datetime.now()

                # Pruning expired nearby devices in order to fill devices caches
                self.__devices_manager.prune_nearby_devices(now)

                # Trying to publish minute stats
                payload = self.__devices_manager.dump_and_clear_minute_data(now, last_minute_stats_time)
                if payload!=None:
                    timestamp               = last_minute_stats_time.replace(second=59)
                    last_minute_stats_time  = now.replace(microsecond=0, second=0)
                    self.__client.publish_minute_statistics(self.__client.MINUTE_STATISTICS_INTERFACE, payload, timestamp)
                
                # Trying to publish hourly stats
                payload = self.__devices_manager.dump_and_clear_hourly_data(now, last_hourly_stats_time)
                if payload!=None:
                    timestamp               = last_hourly_stats_time.replace(second=59, minute=59)
                    last_hourly_stats_time  = now.replace(microsecond=0, second=0, minute=0)
                    self.__client.publish_hourly_statistics(self.__client.HOURLY_STATISTICS_INTERFACE, payload, timestamp)
                
                # Trying to publish daily stats
                payload = self.__devices_manager.dump_and_clear_daily_data(now, last_daily_stats_time)
                if payload!=None:
                    timestamp               = last_hourly_stats_time.replace(second=59, minute=59, hour=23)
                    last_daily_stats_time   = now.replace(microsecond=0, second=0, minute=0, hour=0)
                    self.__client.publish_daily_statistics(self.__client.DAILY_STATISTICS_INTERFACE, payload, timestamp)

                # Trying to generate new devices
                self.__devices_manager.generate_nearby_devices(now)


        except Exception as e:
            print("Catched following exception!!")
            traceback.print_exc()