
import os, glob, json, enum
from pathlib import Path
from datetime import datetime
from astarte.device import Device


class ContainerStatus(enum.Enum):
    CONTAINER_OFF_ALARM_EVENT   = "CONTAINER_OFF_ALARM_EVENT"
    CONTAINER_OPEN_ALARM_EVENT  = "CONTAINER_OPEN_ALARM_EVENT"
    CONTAINER_FULL_ALARM_EVENT  = "CONTAINER_FULL_ALARM_EVENT"


class WaterStatus(enum.Enum):
    WATER_OFF_ALARM_EVENT   = "WATER_OFF_ALARM_EVENT"
    WATER_OPEN_ALARM_EVENT  = "WATER_OPEN_ALARM_EVENT"
    WATER_EMPTY_ALARM_EVENT = "WATER_EMPTY_ALARM_EVENT"


class AstarteClient :

    __COUNTERS_INTERFACE    = "ai.clea.examples.machine.Counters"
    __STATUS_INTERFACE      = "ai.clea.examples.machine.Status"

    __device        = None
    __device_id     = None
    __api_base_url  = None
    __realm         = None
    __loop          = None


    def __init__(self, device_id, realm_name, credentials_secret, api_base_url, persistency_path, interfaces_folder, loop) -> None:

        self.__device_id        = device_id
        self.__api_base_url     = api_base_url
        self.__realm            = realm_name
        self.__loop             = loop

        if not os.path.exists(persistency_path) :
            print ("Directory at path "+persistency_path+" does not exists. Creating it...\n")
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

    def __disconnecton_cb(self, dvc, code) :
        print ('====================\nDevice disconnected!\n====================\n\n')
    
    def __data_cb(self, astarte_device, interface, path, data) :
        print ("Received server data")
    
    def __aggregated_data_cb(self, device, ifname, ifpath, data) :
        print ("Received aggregated server data")

    
    def __build_appengine_url(self):
        return f"{self.__api_base_url}/appengine/v1/{self.__realm}/devices/{self.__device_id}"
    

    ##### ================================ #####


    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def send_short_coffee_count(self, count):
        self.__device.send (self.__COUNTERS_INTERFACE, "/shortCoffee", count)
    

    def send_long_coffee_count(self, count):
        self.__device.send (self.__COUNTERS_INTERFACE, "/longCoffee", count)


    def publish_container_status(self, container_status:ContainerStatus):
        self.__device.send (self.__STATUS_INTERFACE, "/containerStatus", container_status.value)


    def publish_water_status(self, water_status:WaterStatus):
        self.__device.send (self.__STATUS_INTERFACE, "/waterStatus", water_status.value)