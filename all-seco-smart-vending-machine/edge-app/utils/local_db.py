
from utils import commons
from components.astarteClient import AstarteClient

import os
from configparser import ConfigParser


class LocalDB:

    __logger                        = None
    __config                        = None
    __sold_products                 = None
    __astarte_client:AstarteClient  = None
    __max_products_count:int        = None
    ##########


    def __init__(self, config, astarte_client:AstarteClient) -> None:
        self.__logger               = commons.create_logger(__name__)
        self.__config               = config
        self.__astarte_client       = astarte_client
        self.__max_products_count   = int(config['products']['max_products_count'])

        changes_performerd  = False
        products_details    = astarte_client.get_products_details()["data"]
        sold_products       = astarte_client.get_sale_product_details()["data"]
        
        # Creating not existing products
        sold_keys           = sold_products.keys()
        self.__logger.debug(f"Keys are: {sold_keys}")
        for p in products_details:
            if not p in sold_keys:
                changes_performerd  = True
                self.__create_product_item(p)

        # Building local products DB
        if changes_performerd:
            self.__logger.debug(f"Retrieving from cloud!!!!")
            self.__sold_products    = astarte_client.get_sale_product_details()["data"]
        else:
            self.__sold_products    = sold_products
        
        #self.__logger.debug(f"Current sold products:\n{commons.dict_to_pretty_print(self.__sold_products)}")


    def __create_product_item(self, product_id) -> None:
        self.__logger.debug(f"Creating entry for product {product_id}")
        self.__astarte_client.send_sold_product_detail(product_id, "totalSalesCount", 0)
        self.__astarte_client.send_sold_product_detail(product_id, "totalProductCost", 0)
        self.__astarte_client.send_sold_product_detail(product_id, "totalProductPrice", 0)
        self.__astarte_client.send_sold_product_detail(product_id, "remainingItems", 0)
        self.__astarte_client.send_sold_product_detail(product_id, "maxItemsCount", self.__max_products_count)


    def __update_product_values(self, product_id) -> None:
        for k in self.__sold_products[product_id]:
            self.__logger.debug(f"Updating {k} with {self.__sold_products[product_id][k]}")
            self.__astarte_client.send_sold_product_detail(product_id, k, self.__sold_products[product_id][k])


    def refill_event(self) -> None:
        self.__logger.debug("Handling refill event!!!!\n\n\n")
        for p in self.__sold_products:
            self.__sold_products[p]["remainingItems"]   = self.__max_products_count
            self.__update_product_values(p)


    def update_sold_product(self, product_id:str, selling_cost, selling_price) -> None:
        p   = self.__sold_products[product_id]
        p['totalSalesCount'] += 1
        p['totalProductCost'] += selling_cost
        p['totalProductPrice'] += selling_price
        p['remainingItems'] -= 1
        self.__update_product_values(product_id)


    def get_product_info(self, product_id:str) -> dict:
        return self.__sold_products[product_id]