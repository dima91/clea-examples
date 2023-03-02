
from utils import commons

from PySide6.QtCore import QObject

import json


class SuggestionsStrategies(QObject) :

    __logger        = None
    __config        = None
    __startegies    = None
    ##########


    def __init__(self, config) -> None:
        super().__init__()

        self.__logger       = commons.create_logger(__name__)
        self.__startegies   = json.load(open(config['app']['strategies_file']))
    

    def suggest_products(self, session, available_products):
        result      = None
        i_results   = session.inference_results
        print (f"Retrieving strategies for {session.inference_results}")
        ranges      = self.__startegies[i_results["emotion"]][i_results["gender"]]
        curr_age    = i_results["age"]
        idx         = 0

        for r in ranges:
            s_idx   = r.index('-')
            min_age = int(r[:s_idx])
            max_age = int(r[s_idx+1:])
            if curr_age>=min_age and curr_age<=max_age:
                result  = ranges[r]
                break

        return result
    

    def suggest_promo(self, session, available_promos):
        result  = None
        print (available_promos)
        # TODO Selecting those that can be used
        # TODO Randomly choosing an item
        return result
    

    def suggest_advertisement(self, session, available_advertisements) -> str:
        result  = ""
        print(f"\n\n\n\n\n\n{available_advertisements}")
        # TODO Selecting those that can be used
        # TODO Randomly choosing an item
        ##FIXME TEST
        result="abcdef"
        return result