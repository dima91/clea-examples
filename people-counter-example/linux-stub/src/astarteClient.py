
import os, glob, json
from pathlib import Path
from datetime import datetime
from astarte.device import Device


class AstarteClient :

    # Astarte interfaces
    __SCENE_SETTINGS_INTERFACE  = "ai.clea.examples.SceneSettings"
    __PEOPLE_COUNTER_INTERFACE  = "ai.clea.examples.PeopleCounter"

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

    def __disconnecton_cb(self, dvc, code) :
        print ('===================\nDevice disconnected\n===================\n\n')
    
    def __data_cb(self, astarte_device, interface, path, data) :
        print ("Received server data")
    
    def __aggregated_data_cb(self, device, ifname, ifpath, data) :
        print ("Received aggregated server data")


    ##### ================================ #####


    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()


    def publish_scene_settings(self, scene_settings) -> None:
        payload = []
        for s in scene_settings:
            payload.append(str(scene_settings[s]))
        self.__device.send(self.__SCENE_SETTINGS_INTERFACE, "/scene_zones", payload)
    
    def publish_update_interval(self, interval) -> None:
        self.__device.send(self.__SCENE_SETTINGS_INTERFACE, "/update_interval", interval)


    def send_people_count(self, people:list) -> None:
        
        payload = {
            "people_count"  : len(people),
            "people"        : []
        }

        for p in people:
            payload["people"].append(str(p))
        
        self.__device.send_aggregate(self.__PEOPLE_COUNTER_INTERFACE, "/camera", payload)