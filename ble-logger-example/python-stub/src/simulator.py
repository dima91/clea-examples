
import asyncio, random, holidays, traceback, csv, pytz
from datetime import datetime, timezone
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

    __vendors   = None

    __minute_devices_cache  = None
    __hourly_devices_cache  = None
    __daily_devices_cache   = None

    __accessories_vendors   = None
    __smartphones_vendors   = None
    
    def __init__(self, config, country) -> None:
        self.__config           = config
        self.__holidays         = holidays.country_holidays(country)
        self.__nearby_devices   = {}

        self.__minute_devices_cache = {}
        self.__hourly_devices_cache = {}
        self.__daily_devices_cache  = {}

        self.__vendors  = {}
        vendors_file    = open(self.__config['vendors_file_path'], encoding='utf-8')
        file_reader     = csv.reader(vendors_file)
        # Skipping the first row
        next(file_reader)
        # Adding the 'Unknown' value
        self.__vendors["-1"]    = {"dec_id":"-1", "hex_id":"0xFFFF", "name":"Unknown"}
        # Iterating over file lines
        for row in file_reader:
            id = row[0]
            self.__vendors[id] = {"dec_id": id, "hex_id": row[1], "name": row[2]}

        # Building accessories vendors
        self.__accessories_vendors  = utils.build_weighted_list(self.__config['admitted_accessories_vendors'])

        # Building smartphones vendors
        self.__smartphones_vendors  = utils.build_weighted_list(self.__config['admitted_smartphones_vendors'])


    def __update_local_cache(self, cache, address, device) -> None:
        if not (address in cache):
            if device['presence_time']>self.__config['interaction_min_time_s']:
                device['has_interacted']    = True
            else:
                device['has_interacted']    = False
            cache[address]  = device


    def __get_vendor(self, device_type:DeviceType) -> str:
        # Generating weighted vendor
        target_map  = self.__smartphones_vendors if device_type==DeviceType.SMARTPHONE else self.__accessories_vendors
        weight      = random.uniform(0, 100)
        i           = 0
        while i<len(target_map) and weight>target_map[i]['lower_bound']:
            i += 1
        if i>=len(target_map):
            i   = len(target_map)-1

        vendor_id   = target_map[i]['id']
        return self.__vendors[vendor_id]['name'] \
            if vendor_id in self.__vendors \
            else "Unknown"


    def generate_nearby_devices(self, now:datetime) -> None:
        if not (now.date() in self.__holidays):
            
            generation_probability  = self.__config['generation_probabilities'][str(now.hour)]
            new_devices_range       = self.__config['generation_number_ranges'][str(now.hour)]
            presence_time_range     = self.__config['presence_time_ranges_s'][str(now.hour)]

            if random.random() <= generation_probability:
                devices_count   = random.randint(new_devices_range[0], new_devices_range[1])
                # print(f"Generating {devices_count} devices @ {now}")
                
                for i in range(devices_count):
                    addr            = utils.generate_mac_address()
                    if not (addr in self.__nearby_devices):
                        device_type                 = DeviceType.SMARTPHONE \
                                                        if random.random()<=self.__config['smartphone_probability'] \
                                                        else DeviceType.ACCESSORY
                        device_vendor               = self.__get_vendor(device_type)
                        self.__nearby_devices[addr] = {
                            "presence_time" : random.randint(presence_time_range[0], presence_time_range[1]),
                            "creation_time" : now,
                            "device_type"   : device_type,
                            "device_vendor" : device_vendor
                        }

                        #print(f"Generated device: {self.__nearby_devices[addr]}")


    def prune_nearby_devices(self, now:datetime) -> None:
        #print("Pruning nearby devices")
        to_be_popped    = []
        for addr in self.__nearby_devices:
            item    = self.__nearby_devices[addr]
            if (now-item['creation_time']).total_seconds()>item['presence_time']:
                to_be_popped.append(addr)
                self.__update_local_cache(self.__minute_devices_cache, addr, item)
                self.__update_local_cache(self.__hourly_devices_cache, addr, item)
                self.__update_local_cache(self.__daily_devices_cache, addr, item)
        for addr in to_be_popped:
            self.__nearby_devices.pop(addr)


    def dump_and_clear_minute_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__MINUTE_DELAY_S and len(self.__minute_devices_cache)>0:
            result                      = self.__minute_devices_cache
            self.__minute_devices_cache = {}

        return result
    
    
    def dump_and_clear_hourly_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__HOURLY_DELAY_S and len(self.__hourly_devices_cache)>0:
            result  = {}
            # TODO
            self.__hourly_devices_cache.clear()

        return result
    
    
    def dump_and_clear_daily_data(self, now:datetime, last_time:datetime) -> dict:
        result  = None

        if (now-last_time).total_seconds()>self.__DAILY_DELAY_S and len(self.__daily_devices_cache)>0:
            result  = {}
            # TODO
            self.__daily_devices_cache.clear()

        return result




class Simulator:

    __config            = None
    __timezone          = None
    __client            = None
    __devices_manager   = None

    def __init__(self, config:dict, astarte_client:AstarteClient, timezone:str) -> None:
        
        self.__config           = config
        self.__timezone         = timezone
        self.__client           = astarte_client
        self.__devices_manager  = DevicesManager(self.__config['ble_devices'], self.__config['country'])


    async def run(self) -> None:
        try:
            print ("Running Simulator loop..")

            now                     = datetime.now(pytz.timezone(self.__timezone))
            loop_delay              = self.__config["loop_delay_s"]
            last_minute_stats_time  = now.replace(microsecond=0, second=0)
            last_hourly_stats_time  = last_minute_stats_time.replace(minute=0)
            last_daily_stats_time   = last_minute_stats_time.replace(hour=0)

            while True:
                await asyncio.sleep(loop_delay)
                now = datetime.now(pytz.timezone(self.__timezone))

                # Pruning expired nearby devices in order to fill devices caches
                self.__devices_manager.prune_nearby_devices(now)

                # Trying to publish minute stats
                payload = self.__devices_manager.dump_and_clear_minute_data(now, last_minute_stats_time)
                if payload!=None:
                    timestamp               = last_minute_stats_time.replace(second=59)
                    last_minute_stats_time  = now.replace(microsecond=0, second=0)
                    #print(f"timestamp:{timestamp}\nlast_minute_stats_time:{last_minute_stats_time}")
                    self.__client.publish_minute_statistics(payload, timestamp)
                
                # Trying to publish hourly stats
                payload = self.__devices_manager.dump_and_clear_hourly_data(now, last_hourly_stats_time)
                if payload!=None:
                    timestamp               = last_hourly_stats_time.replace(second=59, minute=59)
                    last_hourly_stats_time  = now.replace(microsecond=0, second=0, minute=0)
                    self.__client.publish_hourly_statistics(payload, timestamp)
                
                # Trying to publish daily stats
                payload = self.__devices_manager.dump_and_clear_daily_data(now, last_daily_stats_time)
                if payload!=None:
                    timestamp               = last_hourly_stats_time.replace(second=59, minute=59, hour=23)
                    last_daily_stats_time   = now.replace(microsecond=0, second=0, minute=0, hour=0)
                    self.__client.publish_daily_statistics(payload, timestamp)

                # Trying to generate new devices
                self.__devices_manager.generate_nearby_devices(now)


        except Exception as e:
            print("Catched following exception!!")
            traceback.print_exc()