
import os, glob, json
from datetime import datetime
from astarte.device import Device


class AstarteClient :

    __AIR_DATA_INTERFACE        = "ai.clea.examples.AirData"
    __EVENTS_HISTORY_INTERFACE  = "ai.clea.examples.EventsHistory" 

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
            path    = os.path.join(interfaces_folder, filename)
            if os.path.isfile(path) :
                print (f"Loading interface in {path}...")
                self.__device.add_interface (json.load(open(path)))


    def __connection_cb(self, dvc) :
        print ('================\nDevice connected\n================\n\n')

    def __disconnecton_cb(self, dvc, code) :
        print ("Device disconnected")
    
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
    

    def send_air_data(self, flow, velocity, pollution):
        now = datetime.now()
        self.__device.send (self.__AIR_DATA_INTERFACE, "/flow", flow, datetime.timestamp(now))
        self.__device.send (self.__AIR_DATA_INTERFACE, "/velocity", velocity, datetime.timestamp(now))
        self.__device.send (self.__AIR_DATA_INTERFACE, "/pollution", pollution, datetime.timestamp(now))


    def publish_event(self, type, measure, note_code):
        pass