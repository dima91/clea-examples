
import asyncio, random, holidays
from datetime import datetime, timedelta
from typing import Tuple

import utils


class DevicesGenerator:
    
    __config                = None
    __holidays              = None
    __last_generation_time  = None

    def __init__(self, config, country) -> None:
        self.__config               = config
        self.__holidays             = holidays.country_holidays(country)
        self.__last_generation_time = datetime.now()


    def generate_device(self, curr_devices_count) -> Tuple[str, int]:
        device_addess   = ""
        time            = random.uniform(self.__config["min_presence_time_s"], self.__config["max_presence_time_s"])
        now             = datetime.now()

        if (now-self.__last_generation_time).total_seconds()>self.__config["creation_delay_s"] and \
            random.random()>self.__config["min_creation_probabilities"][str(now.hour)] and \
            curr_devices_count<self.__config["max_devices_count"] and \
            not now.date() in self.__holidays:
            
            self.__last_generation_time = now
            device_addess               = utils.generate_mac_address()
        
        return device_addess, time
    

class TransactionsGenerator:

    __config                = None
    __holidays              = None
    __last_generation_time  = None
    __products_weights      = None

    def __init__(self, config, country) -> None:
        self.__config               = config
        self.__holidays             = holidays.country_holidays(country)
        self.__last_generation_time = datetime.now()
        self.__products_weights     = []
        # Checking that producs weights summation is equal to one
        tmp_sum = 0
        for p in self.__config["products"]:
            tmp_sum += p["weight"]
            if len(self.__products_weights)==0:
                self.__products_weights.append({"name":p["name"], "lower_bound":p["weight"]})
            else:
                last    = self.__products_weights[-1]
                self.__products_weights.append({"name":p["name"], "lower_bound":p["weight"]+last["lower_bound"]})
        if tmp_sum!=1:
            print(f"Products weitghts summation differs from 1 -> {tmp_sum}")
            raise Exception


    def generate_transaction(self) -> dict:
        descriptor  = None
        now         = datetime.now()

        if (now-self.__last_generation_time).total_seconds()>utils.generate_float_with_error(self.__config["delay_s"], self.__config["delay_error"]) and \
            random.random()>self.__config["min_creation_probabilities"][str(now.hour)] :
            
            self.__last_generation_time = now
            
            # Generating weighted product
            weight  = random.random()
            i       = 0
            while i<len(self.__products_weights) and weight>self.__products_weights[i]["lower_bound"]:
                i += 1
            if i>=len(self.__products_weights):
                i   = len(self.__products_weights)-1


            # Generating a transaction
            product_name    = self.__products_weights[i]["name"]
            # print(product_name)
            # print(weight)
            # print(self.__products_weights)
            # print(list(filter(lambda p: p["name"]==product_name, self.__config["products"])))
            choice          = list(filter(lambda p: p["name"]==product_name, self.__config["products"]))[0]
            suggestion      = self.__config["products"][random.randint(0, len(self.__config["products"])-1)]
            is_rejected     = True if random.uniform(0,1) <= self.__config["rejection_probability"] else False
            descriptor      = {
                "age"           : random.randint(self.__config["min_age"], self.__config["max_age"]),
                "emotion"       : self.__config["emotions"][random.randint(0, len(self.__config["emotions"])-1)],
                "gender"        : self.__config["genders"][random.randint(0, len(self.__config["genders"])-1)],
                "suggestion"    : suggestion["name"],
                "choice"        : choice["name"],
                "price"         : choice["price"],
                "is_rejected"   : is_rejected
            }
        
        return descriptor




class Simulator:

    __config                    = None
    __client                    = None
    __devices_generator         = None
    __current_devices           = None
    __transactions_generator    = None

    def __init__(self, config, astarte_client) -> None:
        
        self.__config                   = config
        self.__client                   = astarte_client
        self.__devices_generator        = DevicesGenerator(self.__config["devices"], self.__config["country"])
        self.__current_devices          = []
        self.__transactions_generator   = TransactionsGenerator(self.__config["transactions"], self.__config["country"])


    async def run(self) -> None:
        try:
            print ("Running Simulator loop..")

            while True:
                await asyncio.sleep(5)

                now             = datetime.now()
                expired_devices = []

                # Trying to generate a new device
                device, presence_time   = self.__devices_generator.generate_device(len(self.__current_devices))
                if device!="":
                    #print (f"Registering a new device! (Current device count {len(self.__current_devices)})")
                    self.__current_devices.append({
                        "device_address"    : device,
                        "creation_time"     : now,
                        "presence_time"     : presence_time
                    })

                # Removing expired devices
                i   = 0
                while i<len(self.__current_devices):
                    d   = self.__current_devices[i]
                    if (now-d["creation_time"]).total_seconds()>d["presence_time"]:
                        # Removing current device
                        expired_devices.append(self.__current_devices.pop(i))
                    else:
                        i += 1
                
                # Publishing expired device
                self.__client.publish_devices(expired_devices)

                # Eventually generating a transaction
                transaction = self.__transactions_generator.generate_transaction()
                if transaction!=None:
                    # Publishing the just created transaction
                    self.__client.publish_transaction(transaction)


        except Exception as e:
            print("Catched following exception!!")
            print(e)