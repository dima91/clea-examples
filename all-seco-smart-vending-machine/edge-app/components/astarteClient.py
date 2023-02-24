
import os, logging, glob, json, requests
from utils import commons
from astarte.device import Device
from PySide6.QtCore import QObject, Signal

class AstarteClient(QObject) :

    ## Public members
    NewConnectionStatus = Signal (bool)
    IncomingData        = Signal (any)


    ## Private members
    __device            = None
    __loop              = None
    __logger            = None
    __config            = None
    __api_base_url      = None
    __realm             = None
    __appengine_token   = None
    __device_id         = None


    def __init__(self, config, loop) -> None:
        astarte_config          = config['astarte']
        self.__config           = astarte_config
        self.__api_base_url     = self.__config['api_base_url']
        self.__realm            = self.__config['realm']
        self.__appengine_token  = self.__config['appengine_token']
        self.__device_id        = self.__config['device_id']

        super().__init__()

        self.__loop     = loop
        self.__logger   = commons.create_logger (__name__)

        # Checking direcotry existence
        persistency_path    = astarte_config['persistency_dir']
        if not os.path.exists(persistency_path) :
            print ("Directory at path "+persistency_path+" does not exists.\nCreating it...")
            os.mkdir (persistency_path)
        elif not os.path.isdir (persistency_path) :
            error_message   = f"File at path {persistency_path} is not a directory"
            print (error_message)
            raise Exception (error_message)

        # Initializing Astarte object
        #   Assigning   loop=None -> callbacks will be executed in current thread
        self.__device   = Device (astarte_config['device_id'], astarte_config['realm'], astarte_config['credentials_secret'],
                                    f"{self.__api_base_url}/pairing", persistency_path, None, astarte_config['ignore_ssl_errors'])
        self.__device.on_connected                  = self.__astarte_connection_cb
        self.__device.on_disconnected               = self.__astarte_disconnecton_cb
        self.__device.on_data_received              = self.__astarte_data_cb
        self.__device.on_aggregate_data_received    = self.__astarte_aggregated_data_cb
        

        # Registering interfaces
        for filename in glob.iglob(f'{astarte_config["interfaces_dir_path"]}/*.json'):
            path    = os.path.join(astarte_config["interfaces_dir_path"], filename)
            if os.path.isfile(path) :
                self.__logger.debug (f"Loading interface in {path}...")
                self.__device.add_interface (json.load(open(path)))


    def __astarte_connection_cb (self, dvc) :
        self.__logger.info ('Device connected')
        self.NewConnectionStatus.emit(True)


    def __astarte_disconnecton_cb (self, dvc, boh) :
        self.__logger.warning ("Device disconnected")
        self.NewConnectionStatus.emit(False)

    
    def __astarte_data_cb (self, data) :
        self.__logger.info ("Received server data")
        # TODO Emit signal

    
    def __astarte_aggregated_data_cb (self, data) :
        self.__logger.info ("Received aggregated server data")
        # TODO Emit signal


    def __build_appengine_url(self):
        return f"{self.__api_base_url}/appengine/v1/{self.__realm}/devices/{self.__device_id}"
    def __build_headers(self):
        return {"Content-Type":"application/json; charset=utf-8", "Authorization":f"Bearer {self.__appengine_token}"}


    def connect_device(self):
        self.__device.connect()


    def disconnect_device(self):
        self.__device.disconnect()


    def is_connected (self) -> bool :
        return self.__device.is_connected()
    

    def get_introspection(self) -> dict:
        result      = {}
        url         = f"{self.__build_appengine_url()}"
        response    = requests.get(url, headers=self.__build_headers())

        if response.status_code == 200:
            result  = json.loads(response.content)
        else:
            raise Exception(f"Cannot get device introspection: {response.reason} ({response.status_code})")

        return result


    

    def get_device_setup(self) -> dict:
        result      = {}
        url         = f"{self.__build_appengine_url()}/ai.clea.examples.vendingMachine.DeviceSetup"
        response    = requests.get(url, headers=self.__build_headers())

        # FIXME
        # if response.status_code == 200:
        #     result  = json.loads(response.content)
        # else:
        #     raise Exception(f"Cannot get device setup: {response.reason} ({response.status_code})")
        #
        # return result
        return json.load(open(self.__config["device_setup_test_file"])) #FIXME Remove me! Only for test
    

    def get_products_details(self, product_id=None) -> dict:
        result      = {}
        url         = f"{self.__build_appengine_url()}/ai.clea.examples.vendingMachine.ProductDetails/{product_id if product_id!=None else ''}"
        response    = requests.get(url, headers=self.__build_headers())

        # FIXME
        # if response.status_code == 200:
        #     result  = json.loads(response.content)
        # else:
        #     raise Exception(f"Cannot get product details: {response.reason} ({response.status_code})")
        #
        # return result
        return json.load(open(self.__config["products_test_file"])) #FIXME Remove me! Only for test