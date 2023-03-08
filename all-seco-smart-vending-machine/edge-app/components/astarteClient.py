
import os, logging, glob, json, requests
from utils import commons
from astarte.device import Device
from PySide6.QtCore import QObject, Signal

class AstarteClient(QObject) :

    ## Public members
    NewConnectionStatus     = Signal(bool)
    AdvertisementDataUpdate = Signal(str, dict)
    DeviceSetupUpdate       = Signal(str, dict)
    ProductDetailsUpdate    = Signal(str, dict)
    PromoDetailsUpdate      = Signal(str, dict)
    RefillEvent             = Signal(str, dict)


    ## Private members
            # Client owned
    __CUSTOMER_DETECTION_INTERFACE      = "ai.clea.examples.vendingMachine.CustomerDetection"
    __TRANSACTION_INTERFACE             = "ai.clea.examples.vendingMachine.Transaction"
    __SALE_PRODUCT_DETAILS_INTERFACE    = "ai.clea.examples.vendingMachine.SaleProductDetails"
    __DEVICE_STATUS_INTERFACE           = "ai.clea.examples.vendingMachine.DeviceStatus"
            # Server owned
    __REFILL_EVENT_INTERFACE            = "ai.clea.examples.vendingMachine.RefillEvent"
    __PROMO_DETAILS_INTERFACE           = "ai.clea.examples.vendingMachine.PromoDetails"
    __ADVERTISEMENT_DETAILS_INTERFACE   = "ai.clea.examples.vendingMachine.AdvertisementDetails"
    __PRODUCT_DETAILS_INTERFACE         = "ai.clea.examples.vendingMachine.ProductDetails"
    __DEVICE_SETUP_INTERFACE            = "ai.clea.examples.vendingMachine.DeviceSetup"

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


    def __astarte_disconnecton_cb (self, dvc, code) :
        self.__logger.warning ("Device disconnected")
        self.NewConnectionStatus.emit(False)

    
    def __astarte_data_cb (self, astarte_device, interface, path, data) :
        self.__logger.info ("Received server data")

        if interface == self.__REFILL_EVENT_INTERFACE:
            self.RefillEvent.emit(path, data)
        else:
            raise Exception(f"Received unexpected data from interface {interface}/{path}")

    
    def __astarte_aggregated_data_cb (self, device, ifname, ifpath, data) :
        self.__logger.info ("Received aggregated server data")
        # TODO Emit signal


    def __build_appengine_url(self):
        return f"{self.__api_base_url}/appengine/v1/{self.__realm}/devices/{self.__device_id}"
    
    def __build_headers(self):
        return {"Content-Type":"application/json;charset=utf-8", "Authorization":f"Bearer {self.__appengine_token}", "Accept":"application/json"}
    
    def __perform_get_request(self, suffix_path):
        url     = f"{self.__build_appengine_url()}{suffix_path if suffix_path!='' else ''}"
        response    = requests.get(url, headers=self.__build_headers())
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise Exception(f"Cannot get data at {suffix_path}: {response.reason} ({response.status_code})")


    def connect_device(self):
        self.__device.connect()


    def disconnect_device(self):
        self.__device.disconnect()


    def is_connected (self) -> bool :
        return self.__device.is_connected()
    

    def get_introspection(self) -> dict:
        return self.__perform_get_request("")


    

    def get_device_setup(self) -> dict:
        return self.__perform_get_request(f"/interfaces/{self.__DEVICE_SETUP_INTERFACE}")
    

    def get_products_details(self, product_id:str = None) -> dict:
        return self.__perform_get_request(f"/interfaces/{self.__PRODUCT_DETAILS_INTERFACE}/{product_id if product_id!=None else ''}")


    def get_advertisements_details(self, advertisement_id:str = None) -> dict:
        try:
            return self.__perform_get_request(f"/interfaces/{self.__ADVERTISEMENT_DETAILS_INTERFACE}/{advertisement_id if advertisement_id!=None else ''}")
        except Exception as e:
            print (f'\n\n[QUERY ERROR]\n{__name__} : {e}')
            return {'data':{}}
    

    def get_promos_details(self, promo_id:str = None) -> dict:
        try:
            return self.__perform_get_request(f"/interfaces/{self.__PROMO_DETAILS_INTERFACE}/{promo_id if promo_id!=None else ''}")
        except Exception as e:
            print (f'\n\n[QUERY ERROR]\n{__name__} : {e}')
            return {'data':{}}
        

    def get_sale_product_details(self, product_id:str=None) -> dict:
        return self.__perform_get_request(f"/interfaces/{self.__SALE_PRODUCT_DETAILS_INTERFACE}/{product_id if product_id!=None else ''}")


    def send_device_location(self, latitude:float, longitude:float) -> None:
        # TODO
        pass


    def send_device_status(self, power_consumption:float, chamber_temperature:float, engine_vibration:float) -> None:
        a_data  = {"powerConsumption":power_consumption, "chamberTemperature":chamber_temperature, "engineVibration":engine_vibration}
        self.__device.send_aggregate(self.__DEVICE_STATUS_INTERFACE, "/status", a_data)
        

    def send_customer_detection(self, duration:int, age:int, emotion:str, shown_advertisement_id:str) -> None:
        a_data  = {"duration":duration, "age":age, "emotion":emotion}
        if shown_advertisement_id != None:
            a_data["shownAdvertisementID"]  = shown_advertisement_id

        self.__device.send_aggregate(self.__CUSTOMER_DETECTION_INTERFACE, '/detection', a_data)


    def send_sold_product_detail(self, product_id:str, property_name, property_value) -> None:
        self.__device.send(self.__SALE_PRODUCT_DETAILS_INTERFACE, f"/{product_id}/{property_name}", property_value)


    def send_transaction(self, product_id:str, payment_mode:str, transaction_id:str, selling_cost:float,
                         selling_price:float, with_promo:bool, is_suggested:bool) -> None:
        a_data  = {"productID":product_id, "paymentMode":payment_mode, "tansactionID":transaction_id, "sellingCost":selling_cost,
                   "sellingPrice":selling_price, "withPromo":with_promo, "isSuggested":is_suggested}
        
        self.__device.send_aggregate(self.__TRANSACTION_INTERFACE, "/transaction", a_data)