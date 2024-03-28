import os, glob, json, time, random, uuid, asyncio
from pathlib import Path
from datetime import datetime, timezone
from astarte.device import DeviceMqtt


class AstarteClient :

    # Astarte interfaces
    __BLE_DEVICES_INTERFACE             = "ai.clea.examples.BLEDevices"
    __TRANSACTION_INTERFACE             = "ai.clea.examples.face.emotion.detection.Transaction"
    __REJECTED_TRANSACTION_INTERFACE    = "ai.clea.examples.face.emotion.detection.RejectedTransaction"
    # Edgehog interfaxces
    __HARDWARE_INFO_INTERFACE                   = "io.edgehog.devicemanager.HardwareInfo"
    __OS_INFO_INTERFACE                         = "io.edgehog.devicemanager.OSInfo"
    __RUNTIME_INFO_INTERFACE                    = "io.edgehog.devicemanager.RuntimeInfo"
    __BASE_IMAGE_INTERFACE                      = "io.edgehog.devicemanager.BaseImage"
    __STORAGE_USAGE_INTERFACE                   = "io.edgehog.devicemanager.StorageUsage"
    __BATTERY_STATUS_INTERFACE                  = "io.edgehog.devicemanager.BatteryStatus"
    __SYSTEM_INFO_INTERFACE                     = "io.edgehog.devicemanager.SystemInfo"
    __SYSTEM_STATUS_INTERFACE                   = "io.edgehog.devicemanager.SystemStatus"
    __GEOLOCATION_INTERFACE                     = "io.edgehog.devicemanager.Geolocation"
    __LED_BEHAVIOR_INTERFACE                    = "io.edgehog.devicemanager.LedBehavior"
    __COMMANDS_INTERFACE                        = "io.edgehog.devicemanager.Commands"
    __FORWARDER_SESSION_REQUEST_INTERFACE       = "io.edgehog.devicemanager.ForwarderSessionRequest"
    __OTA_REQUEST_INTERFACE                     = "io.edgehog.devicemanager.OTARequest"
    __OTA_EVENT_INTERFACE                       = "io.edgehog.devicemanager.OTAEvent"
    __TELEMETRY_INTERFACE                       = "io.edgehog.devicemanager.config.Telemetry"
    __NETWORK_INTERFACE_PROPERTIES_INTERFACE   = "io.edgehog.devicemanager.NetworkInterfaceProperties"
    __WIFI_SCAN_RESULTS_INTERFACE               = "io.edgehog.devicemanager.WiFiScanResults"
    __CELLULAR_CONNECTION_PROPERTIES_INTERFACE  = "io.edgehog.devicemanager.CellularConnectionProperties"
    __CELLULAR_CONNECTION_STATUS_INTERFACE      = "io.edgehog.devicemanager.CellularConnectionStatus"

    __OTA_HANDLER_ACKNOWLEDGE_DURATION_S        = 3
    __OTA_HANDLER_DOWNLOAD_DURATION_S           = 60
    __OTA_HANDLER_DOWNLOAD_STEP_COUNT           = 10
    __OTA_HANDLER_DEPLOYING_DURATION_S          = 120
    __OTA_HANDLER_DEPLOYING_STEP_COUNT          = 10
    __OTA_HANDLER_DEPLOYED_DURATION_S           = 5
    __OTA_HANDLER_REBOOTING_DURATION_S          = 40
    __OTA_HANDLER_ERROR_DURATION_S              = 5

    __device        = None
    __device_id     = None
    __api_base_url  = None
    __realm         = None
    __loop          = None

    ## Edgehog constants
    __HARDWARE_INFO = {
        "cpu" : {
            "architecture" : "x86_64",
            "model" : "35",
            "modelName" : "Intel® Celeron® N3350 Dual Core @ 1.1GHz",
            "vendor" : "GenuineIntel"
        },
        "mem" : {
            "totalBytes" : 8389934592
        }
    }
    
    __OS_INFO = {
        "osName" : "Ubuntu",
        "osVersion" : "20.04"
    }

    __RUNTIME_INFO = {
        "name" : "edgehog-device-runtime",
        "url" : "https://github.com/edgehog-device-manager/edgehog-device-runtime",
        "version" : "0.5.0",
        "environment" : "Rust 1.66.1"
    }

    __BASE_IMAGE_DATA = {
        "fingerprint" : "098e55fa9f947c25",
        "name" : "edgehog-app",
        "version" : "0.7.1",
        "buildId" : "20230919154358"
    }

    __STORAGE_USAGE_DATA = {
        "ota_0" : {
            "totalBytes" : 32212254720,
            "freeBytes" : 23085449216
        },
        "ota_1" : {
            "totalBytes" : 32212254720,
            "freeBytes" : 22011707392
        }
    }

    """ __BATTERY_STATUS_DATA = {
        "levelPercentage" : float(100.0),
        "levelAbsoluteError" : float(4.2),
        "status" : "EitherIdleOrCharging"
    } """

    __SYSTEM_INFO = {
        "serialNumber" : "SN000022",
        "partNumber" : "SMART-VENDING-MACHINE"
    }

    __SYSTEM_STATUS_DATA = {
        "availMemoryBytes" : 0,
        "bootId" : "",
        "taskCount" : 0,
        "uptimeMillis" : 0
    }

    __GEOLOCATION_DATA = {
        "latitude" : float(43.459254),
        "longitude" : float(11.822315),
        "altitude" : float(0.0),
        "accuracy" : float(0.0),
        "altitudeAccuracy" : float(0.0),
        "heading" : float(80),
        "speed" : float(0.0)
    }

    __NETWORK_INTERFACES_PROPERTIES_DATA = [
        {'name':'eno1', 'macAddress':'00:c0:08:9d:8f:88', 'technologyType':'Ethernet'},
        {'name':'enp2s0', 'macAddress':'00:c0:08:9d:8f:87', 'technologyType':'Ethernet'}
    ]

    """ __WIFI_SCAN_RESULTS = [
        {"channel":11, "connected":False, "essid":"Pulsar-3bcf", "macAddress":"58:7A:62:3F:3B:CF", "rssi":-53},
        {"channel":11, "connected":False, "essid":"SECO-SI", "macAddress":"BC:22:28:DF:A0:D0", "rssi":-39},
        {"channel":100, "connected":False, "essid":"SECO-SI-GUEST", "macAddress":"BC:22:28:DF:A0:D1", "rssi":-38},
        {"channel":11, "connected":False, "essid":"SECO-DEMO-AP", "macAddress":"FC:44:82:2A:A7:51", "rssi":-48},
        {"channel":1, "connected":False, "essid":"ImpresaVerde", "macAddress":"00:19:3B:1E:75:6C", "rssi":-78},
        {"channel":6, "connected":False, "essid":"Wi-Fi StudioFlori", "macAddress":"76:42:7F:D7:4F:08", "rssi":-75},
        {"channel":6, "connected":False, "essid":"STUDIOCOMMERCIALE", "macAddress":"74:42:7F:D7:4F:08", "rssi":-74},
    ] """

    """ __CELLULAR_CONNECTION_PROPERTIES_DATA = {
        'apn' : 'seco.cxn',
        'imei' : '860016040564713',
        'imsi' : '222299845466094'
    } """
    """ __CELLULAR_CONNECTION_STATUS_DATA = {
        'carrier' : 'TELENOR',
        'cellId' : 143,
        'mobileCountryCode' : 222,
        'mobileNetworkCode' : 299,
        'localAreaCode' : 39,
        'registrationStatus' : 'RegisteredRoaming',
        'rssi' : 0,
        'technology' : 'GSM'
    } """

    __RSSI_RANGE = (-100,0)
    __TASKS_COUNT_RANGE = (90, 120)
    __AVAILABLE_MEM_BYTES_RANGE = (4831838208, 7516192768)


    def __init__(self, device_id, realm_name, credentials_secret, api_base_url, persistency_path, interfaces_folder, loop) -> None:

        self.__device_id        = device_id
        self.__api_base_url     = api_base_url
        self.__realm            = realm_name
        self.__loop             = loop

        self.__start_time_ms                = int(datetime.now(tz=timezone.utc).timestamp()*1000)
        self.__SYSTEM_STATUS_DATA['bootId'] = str(uuid.uuid4())
        self.__current_ota_uuid             = None

        # Initializing "random" module
        random.seed()

        if not os.path.exists(persistency_path) :
            print ("Directory at path "+persistency_path+" does not exists.\nCreating it...")
            os.mkdir (persistency_path)
        elif not os.path.isdir (persistency_path) :
            error_message   = f"File at path {persistency_path} is not a directory"
            print (error_message)
            raise Exception (error_message)

        self.__device   = DeviceMqtt (device_id, realm_name, credentials_secret, f"{api_base_url}/pairing", persistency_path)
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
        print ("Received server data...")
        
        if interface == self.__LED_BEHAVIOR_INTERFACE:
            self.__on_led_behavior(path, data)
        elif interface == self.__COMMANDS_INTERFACE:
            self.__on_server_command(path, data)
        elif interface == self.__FORWARDER_SESSION_REQUEST_INTERFACE:
            self.__on_forwarder_session_request(path, data)
        elif interface == self.__OTA_REQUEST_INTERFACE:
            self.__on_ota_request(path, data)
        elif interface == self.__TELEMETRY_INTERFACE:
            self.__on_telemetry(path, data)
        else:
            print(f"Undefined operation for data received at {path=} of {interface=}")

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
            payload["presence_time"].append(int(d["presence_time"])*1000)
        
        print (f"Devices @ {datetime.now(tz=timezone.utc)}")
        self.__device.send_aggregate(self.__BLE_DEVICES_INTERFACE, "/bleDevices", payload)


    def publish_transaction(self, descriptor) -> None:
        currtime = datetime.now(tz=timezone.utc)
        print (f"Transaction @ {currtime}")
        print (f"Publishing following transaction\n{descriptor}")

        
        payload = {
            "age"           : descriptor["age"] if not descriptor["detection_failed"] else 0,
            "emotion"       : descriptor["emotion"] if not descriptor["detection_failed"] else "None",
            "gender"        : descriptor["gender"] if not descriptor["detection_failed"] else "None",
            "suggestion"    : descriptor["suggestion"] if not descriptor["detection_failed"] else "None",
            "timedate"      : currtime
        }

        if not descriptor["is_rejected"]:
            payload["choice"]   = descriptor["choice"]
            payload["price"]    = float(descriptor["price"])
            self.__device.send_aggregate(self.__TRANSACTION_INTERFACE, "/transaction", payload, currtime)
        else:    
            self.__device.send_aggregate(self.__REJECTED_TRANSACTION_INTERFACE, "/transaction", payload, currtime)



    ## ========================= ##
    ## Edgehog related functions ##
        
    def send_device_info(self):
        self.__publish_hardware_info()
        self.__publish_os_info()
        self.__publish_runtime_info()
        self.__publish_network_interfaces_properties()
        self.__publish_storage_usage()
        self.__publish_system_info()
        self.__publish_geolocation()
        self.__publish_base_image()

        self.update_system_status()


    def ota_update_in_progress(self):
        return self.__current_ota_uuid != None
        

    def __on_server_command(self, path, data):
        print(f"Received server command\n{path=}\n{data=}")


    """ # Remote terminal - not needed
    def __on_forwarder_session_request(self, path, data):
        print(f"Received forwarder session request\n{path=}\n{data=}") """


    """ # Remote terminal - not needed
    def __publish_forwarder_session_state(self):
        print("Publishing forwarder session state") """


    def __on_led_behavior(self, path, data):
        print(f"Received led behavior\n{path=}\n{data=}")


    def __on_ota_request(self, path, data):
        print(f"Received OTA request\n{path=}\n{data=}")

        if self.__current_ota_uuid != None:
            print("VERY DANGEROUS: OTA update already in progress!!")
            self.__publish_error_and_failure(data['uuid'], "UpdateAlreadyInProgress", "")
        else :
            self.__current_ota_uuid = data['uuid']
            self.__loop.create_task(self.__ota_handler())


    def __publish_ota_event(self, payload):
        print(f"Publishing OTA event -> {payload['status']}")
        self.__device.send_aggregate(self.__OTA_EVENT_INTERFACE, "/event", payload, datetime.now(tz=timezone.utc))

    def __publish_error_and_failure(self, request_uuid:str, status_code:str, message:str):
        # Sending error status
        self.__publish_ota_event(self.__build_error_payload(request_uuid, status_code, message))
        time.sleep(self.__OTA_HANDLER_ERROR_DURATION_S)
        # Sending failure result
        self.__publish_ota_event(self.__build_failure_payload(request_uuid, status_code, message))

    
    def __build_aknowledgd_payload(self):
        return {"requestUUID":self.__current_ota_uuid, "status":"Acknowledged", "statusProgress":100,
                "statusCode":"", "message":""}
    
    def __build_downloading_payload(self, status_progress:float):
        return {"requestUUID":self.__current_ota_uuid, "status":"Downloading", "statusProgress":int(status_progress),
                "statusCode":"", "message":""}

    def __build_deploying_payload(self, status_progress:float):
        return {"requestUUID":self.__current_ota_uuid, "status":"Deploying", "statusProgress":int(status_progress),
                "statusCode":"", "message":""}
    
    def __build_deployed_payload(self):
        return {"requestUUID":self.__current_ota_uuid, "status":"Deployed", "statusProgress":100,
                "statusCode":"", "message":""}
    
    def __build_rebooting_payload(self):
        return {"requestUUID":self.__current_ota_uuid, "status":"Rebooting", "statusProgress":100,
                "statusCode":"", "message":""}
    
    def __build_success_payload(self):
        return {"requestUUID":self.__current_ota_uuid, "status":"Success", "statusProgress":100,
                "statusCode":"", "message":""}
    
    def __build_error_payload(self, request_uuid, status_code, message):
        return {"requestUUID":request_uuid, "status":"Error", "statusProgress":100,
                "statusCode":status_code, "message":message}
    
    def __build_failure_payload(self, request_uuid, status_code, message):
        return {"requestUUID":request_uuid, "status":"Failure", "statusProgress":100,
                "statusCode":status_code, "message":message}


    async def __ota_handler(self):
        print("Handling OTA..")
        current_step_number = 0
        current_step_delay_s = 0

        # Sending acknowledge
        self.__publish_ota_event(self.__build_aknowledgd_payload())
        await asyncio.sleep(self.__OTA_HANDLER_ACKNOWLEDGE_DURATION_S)

        # Simulating binary file downloading
        current_step_number = 0
        current_step_delay_s = float(self.__OTA_HANDLER_DOWNLOAD_DURATION_S / self.__OTA_HANDLER_DOWNLOAD_STEP_COUNT)
        while current_step_number < self.__OTA_HANDLER_DOWNLOAD_STEP_COUNT:
            await asyncio.sleep(current_step_delay_s)
            # Publishing download event update
            current_step_number = current_step_number+1
            self.__publish_ota_event(self.__build_downloading_payload((100/self.__OTA_HANDLER_DOWNLOAD_STEP_COUNT)*current_step_number))

        # Simulating image deploy
        current_step_number = 0
        current_step_delay_s = float(self.__OTA_HANDLER_DEPLOYING_DURATION_S / self.__OTA_HANDLER_DEPLOYING_STEP_COUNT)
        while current_step_number < self.__OTA_HANDLER_DEPLOYING_STEP_COUNT:
            await asyncio.sleep(current_step_delay_s)
            # Publishing deploying event update
            current_step_number = current_step_number+1
            self.__publish_ota_event(self.__build_deploying_payload((100/self.__OTA_HANDLER_DEPLOYING_STEP_COUNT)*current_step_number))

        # Sending deployed result
        self.__publish_ota_event(self.__build_deployed_payload())
        await asyncio.sleep(self.__OTA_HANDLER_DEPLOYED_DURATION_S)
        
        # Sending rebooting result
        self.__publish_ota_event(self.__build_rebooting_payload())
        await asyncio.sleep(self.__OTA_HANDLER_REBOOTING_DURATION_S)
        
        # Sending success result
        self.__publish_ota_event(self.__build_success_payload())

        self.__current_ota_uuid = None


    def __on_telemetry(self):
        # TODO
        print("Received telemetry update")


    def __publish_hardware_info(self):
        print("Publishing hardware info..")
        self.__device.send(self.__HARDWARE_INFO_INTERFACE, "/cpu/architecture", self.__HARDWARE_INFO["cpu"]["architecture"])
        self.__device.send(self.__HARDWARE_INFO_INTERFACE, "/cpu/model", self.__HARDWARE_INFO["cpu"]["model"])
        self.__device.send(self.__HARDWARE_INFO_INTERFACE, "/cpu/modelName", self.__HARDWARE_INFO["cpu"]["modelName"])
        self.__device.send(self.__HARDWARE_INFO_INTERFACE, "/cpu/vendor", self.__HARDWARE_INFO["cpu"]["vendor"])
        self.__device.send(self.__HARDWARE_INFO_INTERFACE, "/mem/totalBytes", self.__HARDWARE_INFO["mem"]["totalBytes"])


    def __publish_network_interfaces_properties(self):
        print("Publishing network interfaces properties")
        for item in self.__NETWORK_INTERFACES_PROPERTIES_DATA:
            self.__device.send(self.__NETWORK_INTERFACE_PROPERTIES_INTERFACE, f'/{item["name"]}/macAddress', item['macAddress'])
            self.__device.send(self.__NETWORK_INTERFACE_PROPERTIES_INTERFACE, f'/{item["name"]}/technologyType', item['technologyType'])
            


    def __publish_os_info(self):
        print("Publishing OS info")
        self.__device.send(self.__OS_INFO_INTERFACE, "/osName", self.__OS_INFO["osName"])
        self.__device.send(self.__OS_INFO_INTERFACE, "/osVersion", self.__OS_INFO["osVersion"])


    def __publish_runtime_info(self):
        print("Publishing runtime info")
        self.__device.send(self.__RUNTIME_INFO_INTERFACE, "/name", self.__RUNTIME_INFO["name"])
        self.__device.send(self.__RUNTIME_INFO_INTERFACE, "/url", self.__RUNTIME_INFO["url"])
        self.__device.send(self.__RUNTIME_INFO_INTERFACE, "/version", self.__RUNTIME_INFO["version"])
        self.__device.send(self.__RUNTIME_INFO_INTERFACE, "/environment", self.__RUNTIME_INFO["environment"])


    def __publish_base_image(self):
        print("Publishing base image")
        self.__device.send(self.__BASE_IMAGE_INTERFACE, "/fingerprint", self.__BASE_IMAGE_DATA["fingerprint"])
        self.__device.send(self.__BASE_IMAGE_INTERFACE, "/name", self.__BASE_IMAGE_DATA["name"])
        self.__device.send(self.__BASE_IMAGE_INTERFACE, "/version", self.__BASE_IMAGE_DATA["version"])
        self.__device.send(self.__BASE_IMAGE_INTERFACE, "/buildId", self.__BASE_IMAGE_DATA["buildId"])


    """ No battery
    def __publish_battery_status(self):
        print("Publishing battery status") """


    """ No cellular modem
    def __publish_cellular_connection_properties(self):
        print("Publishing cellular connection properties") """


    """ No cellular modem
    def __publish_cellular_connection_status(self):
        print("Publishing cellular connection status") """


    def __publish_geolocation(self):
        print("Publishing geolocation")
        self.__device.send_aggregate(self.__GEOLOCATION_INTERFACE, "/gps", self.__GEOLOCATION_DATA, datetime.now(tz=timezone.utc))


    def __publish_storage_usage(self):
        print("Publishing storage usage")
        now = datetime.now(tz=timezone.utc)
        self.__device.send_aggregate(self.__STORAGE_USAGE_INTERFACE, "/ota_0", self.__STORAGE_USAGE_DATA["ota_0"], now)
        self.__device.send_aggregate(self.__STORAGE_USAGE_INTERFACE, "/ota_1", self.__STORAGE_USAGE_DATA["ota_1"], now)


    def __publish_system_info(self):
        print("Publishing system info")
        self.__device.send(self.__SYSTEM_INFO_INTERFACE, "/serialNumber", self.__SYSTEM_INFO['serialNumber'])
        self.__device.send(self.__SYSTEM_INFO_INTERFACE, "/partNumber", self.__SYSTEM_INFO['partNumber'])



    def __publish_system_status(self):
        print("Publishing system status")
        self.__device.send_aggregate(self.__SYSTEM_STATUS_INTERFACE, "/systemStatus", self.__SYSTEM_STATUS_DATA, datetime.now(tz=timezone.utc))


    """ No wifi transceiver
    def __publish_wifi_scan_result(self):
        print("Publishing wifi scan result") """

    
    ### ================== ###
    ### ================== ###
        
    def update_device_uptime(self):
        msts_now = int(datetime.now(tz=timezone.utc).timestamp()*1000)
        uptime_ms = msts_now - self.__start_time_ms
        self.__SYSTEM_STATUS_DATA["uptimeMillis"] = uptime_ms
        self.__publish_system_status()


    def update_system_status(self):
        self.__SYSTEM_STATUS_DATA["taskCount"] = random.randrange(self.__TASKS_COUNT_RANGE[0], self.__TASKS_COUNT_RANGE[1])
        self.__SYSTEM_STATUS_DATA["availMemoryBytes"] = random.randrange(self.__AVAILABLE_MEM_BYTES_RANGE[0], self.__AVAILABLE_MEM_BYTES_RANGE[1])
        self.update_device_uptime()

    
    """ No wifi transceiver
    def update_wifi_scan_results(self):
        for item in self.__WIFI_SCAN_RESULTS:
            item['rssi'] = random.randrange(self.__RSSI_RANGE[0], self.__RSSI_RANGE[1])
        self.__publish_wifi_scan_result() """

    
    """ No cellular modem
    def update_cellular_connection_status(self):
        self.__CELLULAR_CONNECTION_STATUS_DATA['rssi'] = float(random.randrange(self.__RSSI_RANGE[0], self.__RSSI_RANGE[1]))
        self.__publish_cellular_connection_status() """
