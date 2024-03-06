
import os, glob, json
from pathlib import Path
from datetime import datetime
from astarte.device import DeviceMqtt
from utils import DayPeriod


class AstarteClient :

    # Astarte interfaces
    __EXTERNAL_SENSORS_INTERFACE    = "ai.clea.examples.offgrid.ExternalSensors"
    __BATTERY_STATS_INTERFACE       = "ai.clea.examples.offgrid.BatteryStats"
    __LOAD_STATS_INTERFACE          = "ai.clea.examples.offgrid.LoadStats"
    __PANEL_STATS_INTERFACE         = "ai.clea.examples.offgrid.PanelStats"

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

        self.__device   = DeviceMqtt (device_id=device_id,
                                      realm=realm_name,
                                      credentials_secret=credentials_secret,
                                      pairing_base_url=f"{api_base_url}/pairing",
                                      persistency_dir=persistency_path
                                      )
        self.__device.set_events_callbacks(on_connected=self.__connection_cb, on_data_received=self.__data_cb, on_disconnected=self.__disconnecton_cb, loop=self.__loop)

        # Adding used interfaces
        for filename in glob.iglob(f'{interfaces_folder}/*.json'):
            if os.path.isfile(filename) :
                print (f"Loading interface in {filename}...")
                self.__device.add_interface_from_json (json.load(open(filename)))
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


    def __build_external_sensor_payload(self, value, sensor_type, display_string) -> dict:
        return {
            "sensorValue"           : float(value),
            "sensorType"            : sensor_type,
            "sensorDisplayString"   : display_string
        }
    
    def __build_stats_payload(self, voltage:float, current:float) -> dict:
        return {
            "voltage"   : float(voltage),
            "current"   : float(current)
        }


    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def publish_day_period(self, day_period:DayPeriod) -> None:
        self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/day_period",
                                    self.__build_external_sensor_payload(day_period.value, "day_period", "day_period"))

    def publish_reference_current(self, value:float) -> None:
        self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/reference_electrical_current",
                                    self.__build_external_sensor_payload(value, "reference_electrical_current", "reference_electrical_current"))

    def publish_temperature(self, value:float) -> None:
        self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/temperature",
                                    self.__build_external_sensor_payload(value, "temperature", "temperature"))
    
    def publish_wind_speed(self, value:float) -> None:
        self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/wind_velocity",
                                    self.__build_external_sensor_payload(value, "wind_velocity", "wind_velocity"))
        
    
    def publish_panel_stats(self, voltage:float, current:float) -> None:
        self.__device.send_aggregate(self.__PANEL_STATS_INTERFACE, "/panel", self.__build_stats_payload(voltage, current))

    def publish_battery_stats(self, voltage:float, current:float) -> None:
        self.__device.send_aggregate(self.__BATTERY_STATS_INTERFACE, "/battery", self.__build_stats_payload(voltage, current))
    
    def publish_load_stats(self, voltage:float, current:float) -> None:
        self.__device.send_aggregate(self.__LOAD_STATS_INTERFACE, "/load", self.__build_stats_payload(voltage, current))