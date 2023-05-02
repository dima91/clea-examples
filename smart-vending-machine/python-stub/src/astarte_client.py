
import os, glob, json
from pathlib import Path
from datetime import datetime
from astarte.device import Device


class AstarteClient :

    # Astarte interfaces
    __BLE_DEVICES_INTERFACE             = "ai.clea.examples.BLEDevices"
    __TRANSACTION_INTERFACE             = "ai.clea.examples.face.emotion.detection.Transaction"
    __REJECTED_TRANSACTION_INTERFACE    = "ai.clea.examples.face.emotion.detection.RejectedTransaction"

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


    # def __build_external_sensor_payload(self, value, sensor_type, display_string) -> dict:
    #     return {
    #         "sensorValue"           : value,
    #         "sensorType"            : sensor_type,
    #         "sensorDisplayString"   : display_string
    #     }
    
    # def __build_stats_payload(self, voltage:float, current:float) -> dict:
    #     return {
    #         "voltage"   : voltage,
    #         "current"   : current
    #     }

    ########################################

    def connect(self):
        self.__device.connect()
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def publish_devices(self, devices) -> None:
        payload = {
            "devices"       : [],
            "presence_time" : []
        }
        for d in devices:
            payload["devices"].append(d["device_address"])
            payload["presence_time"].append(int(d["presence_time"]))
        
        self.__device.send_aggregate(self.__BLE_DEVICES_INTERFACE, "/", payload)


    def publish_transaction(self) -> None:
        # TODO
        pass


    def publish_rejected_transaction(self) -> None:
        # TODO
        pass
    

    # def publish_day_period(self, day_period:DayPeriod) -> None:
    #     self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/day_period",
    #                                 self.__build_external_sensor_payload(day_period.value, "day_period", "day_period"))

    # def publish_reference_current(self, value:float) -> None:
    #     self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/reference_electrical_current",
    #                                 self.__build_external_sensor_payload(value, "reference_electrical_current", "reference_electrical_current"))

    # def publish_temperature(self, value:float) -> None:
    #     self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/temperature",
    #                                 self.__build_external_sensor_payload(value, "temperature", "temperature"))
    
    # def publish_wind_speed(self, value:float) -> None:
    #     self.__device.send_aggregate(self.__EXTERNAL_SENSORS_INTERFACE, "/wind_velocity",
    #                                 self.__build_external_sensor_payload(value, "wind_velocity", "wind_velocity"))
        
    
    # def publish_panel_stats(self, voltage:float, current:float) -> None:
    #     self.__device.send_aggregate(self.__PANEL_STATS_INTERFACE, "/", self.__build_stats_payload(voltage, current))

    # def publish_battery_stats(self, voltage:float, current:float) -> None:
    #     self.__device.send_aggregate(self.__BATTERY_STATS_INTERFACE, "/", self.__build_stats_payload(voltage, current))
    
    # def publish_load_stats(self, voltage:float, current:float) -> None:
    #     self.__device.send_aggregate(self.__LOAD_STATS_INTERFACE, "/", self.__build_stats_payload(voltage, current))