
import os, logging, glob, json
from utils import commons
from astarte.device import Device
from PySide6.QtCore import QObject, Signal

class AstarteClient(QObject) :

    ## Public members
    NewConnectionStatus = Signal (bool)
    IncomingData        = Signal (any)


    ## Private members
    __device    = None
    __loop      = None
    __logger    = None


    def __init__(self, config, loop) -> None:
        astarte_config  = config['astarte']

        super().__init__()

        self.__loop     = loop
        self.__logger   = commons.create_logger (logging, __name__)

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
                                    astarte_config['pairing_base_url'], persistency_path, None, astarte_config['ignore_ssl_errors'])
        self.__device.on_connected                  = self.__astarte_connection_cb
        self.__device.on_disconnected               = self.__astarte_disconnecton_cb
        self.__device.on_data_received              = self.__astarte_data_cb
        self.__device.on_aggregate_data_received    = self.__astarte_aggregated_data_cb
        

        # Registering interfaces
        for filename in glob.iglob(f'{astarte_config["interfaces_dir_path"]}/*.json'):
            path    = os.path.join(astarte_config["interfaces_dir_path"], filename)
            if os.path.isfile(path) :
                print (f"Loading interface in {path}...")
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


    def connect_device(self):
        self.__device.connect()


    def disconnect_device(self):
        self.__device.disconnect()


    def is_connected (self) -> bool :
        return self.__device.is_connected()