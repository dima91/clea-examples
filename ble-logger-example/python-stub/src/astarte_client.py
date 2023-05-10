
import os, glob, json
from pathlib import Path
from datetime import datetime

from astarte.device import Device
from utils import DeviceType


class AstarteClient :

    # Astarte interfaces
    MINUTE_STATISTICS_INTERFACE = "ai.clea.examples.blelogger.MinuteStats"
    HOURLY_STATISTICS_INTERFACE = "ai.clea.examples.blelogger.HourlyStats"
    DAILY_STATISTICS_INTERFACE  = "ai.clea.examples.blelogger.DailyStats"

    __device            = None
    __device_id         = None
    __api_base_url      = None
    __realm             = None
    __loop              = None
    __on_connection_cb  = None


    def __init__(self, device_id, realm_name, credentials_secret, api_base_url, persistency_path, interfaces_folder,
                 loop, on_connection_cb) -> None:

        self.__device_id        = device_id
        self.__api_base_url     = api_base_url
        self.__realm            = realm_name
        self.__loop             = loop
        self.__on_connection_cb = on_connection_cb

        if not os.path.exists(persistency_path) :
            print ("Directory at path "+persistency_path+" does not exists.\nCreating it...")
            os.mkdir (persistency_path)
        elif not os.path.isdir (persistency_path) :
            error_message   = f"File at path {persistency_path} is not a directory"
            print (error_message)
            raise Exception (error_message)

        self.__device   = Device (device_id, realm_name, credentials_secret, f"{api_base_url}/pairing", persistency_path, loop)

        self.__device.on_connected                  = self.__connection_cb
        self.__device.on_disconnected               = self.__disconnecton_cb
        self.__device.on_data_received              = self.__data_cb
        self.__device.on_aggregate_data_received    = self.__aggregated_data_cb

        # Adding used interfaces
        for filename in glob.iglob(f'{interfaces_folder}/*.json'):
            if os.path.isfile(filename) :
                print (f"Loading interface in {filename}...")
                self.__device.add_interface (json.load(open(filename)))
            else:
                print (f"File {filename} is not file!")


    def __connection_cb(self, dvc) :
        print ('================\nDevice connected\n================\n\n')
        self.__on_connection_cb()

    def __disconnecton_cb(self, dvc, code) :
        print ('===================\nDevice disconnected\n===================\n\n')
    
    def __data_cb(self, astarte_device, interface, path, data) :
        print ("Received server data")
    
    def __aggregated_data_cb(self, device, ifname, ifpath, data) :
        print ("Received aggregated server data")


    def __prepare_astarte_payload(self, stats) -> dict:
        accessories         = []
        accessories_vendors = {}
        smartphones         = []
        smartphones_vendors = {}
        interactions        = []    # Computed only on smartphones

        for addr in stats :
            item    = stats[addr]
            if item['device_type'] == DeviceType.ACCESSORY:
                accessories.append(addr)
                accessories_vendors[item['device_vendor']]  = addr
            elif item['device_type'] == DeviceType.SMARTPHONE:
                smartphones.append(addr)
                smartphones_vendors[item['device_vendor']]  = addr
                # Checking if interaction is present
                if item['has_interacted']:
                    interactions.append(item['presence_time'])

        return {
            "accessoriesVendors"    : json.dumps(accessories_vendors),
            "detectedAccessories"   : accessories,
            "smartphonesVendors"    : json.dumps(smartphones_vendors),
            "detectedSmartphones"   : smartphones,
            "interactions"          : interactions
        }
    

    def __publish_statistics(self, interface, payload, timestamp) -> None:
        self.__device.send_aggregate(interface, "/", payload, timestamp)

    ########################################

    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def publish_minute_statistics(self, stats, timestamp) -> None:
        self.__publish_statistics(self.MINUTE_STATISTICS_INTERFACE, self.__prepare_astarte_payload(stats), timestamp)


    def publish_hourly_statistics(self, stats, timestamp) -> None:
        self.__publish_statistics(self.HOURLY_STATISTICS_INTERFACE, self.__prepare_astarte_payload(stats), timestamp)


    def publish_daily_statistics(self, stats, timestamp) -> None:
        self.__publish_statistics(self.DAILY_STATISTICS_INTERFACE, self.__prepare_astarte_payload(stats), timestamp)
