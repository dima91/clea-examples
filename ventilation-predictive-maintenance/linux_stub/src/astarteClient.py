
import os, glob, json
from datetime import datetime
from astarte.device import Device


class AstarteClient :

    __AIR_DATA_INTERFACE        = "ai.clea.examples.AirData"
    __EVENTS_HISTORY_INTERFACE  = "ai.clea.examples.EventsHistory"

    MAX_FLOW        = 1.0
    MIN_FLOW        = 0.0
    MAX_SPEED       = 25.0
    MAX_POLLUTION   = 50.0
    MIN_POLLUTION   = 0.0
    
    WARNING_FLOW        = 0.7
    __DANGER_FLOW       = 0.5
    WARNING_POLLUTION   = 20.0
    __DANGER_POLLUTION  = 35.0
    __WARNING_NOTE      = 1
    __DANGER_NOTE       = 2
    __FLOW_EVENT        = 111
    __POLLUTION_EVENT   = 222

    __flow_warning_detected         = False
    __flow_danger_detected          = False
    __pollution_warning_detected    = False
    __pollution_danger_detected     = False

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
    

    def __flow_2_speed(self, flow):
        return self.MAX_SPEED*flow
    

    ##### ================================ #####


    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def send_air_data(self, flow, pollution):
        now     = datetime.now()
        speed   = self.__flow_2_speed(flow)
        self.__device.send (self.__AIR_DATA_INTERFACE, "/flow", flow, datetime.timestamp(now))
        self.__device.send (self.__AIR_DATA_INTERFACE, "/velocity", speed, datetime.timestamp(now))
        self.__device.send (self.__AIR_DATA_INTERFACE, "/pollution", pollution, datetime.timestamp(now))

        # Checking for flow alerts
        if flow<self.__DANGER_FLOW:
            if not self.__flow_danger_detected:
                self.__flow_danger_detected = True
                self.publish_event(self.__FLOW_EVENT, flow, self.__DANGER_NOTE)
        else:
            if flow<self.WARNING_FLOW:
                if not self.__flow_danger_detected and not self.__flow_warning_detected:
                    self.__flow_warning_detected    = True
                    self.publish_event(self.__FLOW_EVENT, flow, self.__WARNING_NOTE)
            else:
                self.__flow_danger_detected     = False
                self.__flow_warning_detected    = False


        # Checking for pollution alerts
        if pollution>self.__DANGER_POLLUTION:
            if not self.__pollution_danger_detected:
                self.__pollution_danger_detected    = True
                self.publish_event(self.__POLLUTION_EVENT, pollution, self.__DANGER_NOTE)
        else:
            if pollution>self.WARNING_POLLUTION:
                if not self.__pollution_danger_detected and not self.__pollution_warning_detected:
                    self.__pollution_warning_detected    = True
                    self.publish_event(self.__POLLUTION_EVENT, pollution, self.__WARNING_NOTE)
            else:
                self.__pollution_danger_detected    = False
                self.__pollution_warning_detected   = False
        


    def publish_event(self, type, measure, note_code):
        detection   = None

        if type==self.__FLOW_EVENT:
            detection   = "Flow"
        elif type==self.__POLLUTION_EVENT:
            detection   = "Pollution"
        else:
            raise Exception(f"Wrong event type: {type}")
        
        a_data  = {
            "detection" : detection,
            "measure"   : measure,
            "noteCode"  : note_code
        }

        print (f"Sending {a_data}")
        
        self.__device.send_aggregate(self.__EVENTS_HISTORY_INTERFACE, "/event", a_data)