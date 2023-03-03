
from utils import commons

from PySide6.QtCore import QObject

import json, typing, random
from datetime import datetime
from dateutil import parser


class SuggestionsStrategies(QObject) :

    __logger        = None
    __config        = None
    __startegies    = None
    ##########


    def __init__(self, config) -> None:
        super().__init__()

        self.__logger       = commons.create_logger(__name__)
        self.__startegies   = json.load(open(config['app']['strategies_file']))


    def __check_schedule_time(self, start_schedule_time:str, end_schedule_time:str) -> bool:
        # "start_schedule_time" and "end_schedule_time" are in the form "hh:mm"
        now             = datetime.now()
        idx             = start_schedule_time.index(":")
        start_datetime  = now.replace(hour=int(start_schedule_time[:idx]), minute=int(start_schedule_time[idx+1:]), microsecond=0)
        idx             = end_schedule_time.index(":")
        end_datetime    = now.replace(hour=int(end_schedule_time[:idx]), minute=int(end_schedule_time[idx+1:]), microsecond=0)
        print (f"start:{start_datetime.time()}\tnow:{now.time()}\tend:{end_datetime.time()}")
        return now.time()>start_datetime.time() and now.time()<end_datetime.time()
    
    def __check_date_range(self, start_date, end_date) -> bool:
        now             = datetime.now()
        start_datetime  = parser.parse(start_date)
        end_datetime    = parser.parse(end_date)
        print (f"start:{start_datetime}\tnow:{now}\tend:{end_datetime}")
        return now.timestamp()>start_datetime.timestamp() and now.timestamp()<end_datetime.timestamp()
    
    def __check_inference_results(self, session, min_age, max_age, target_emotions) -> bool:
        curr_age        = session.inference_results['age']
        curr_emotion    = session.inference_results['emotion']
        return curr_age>=min_age and curr_age<=max_age and curr_emotion in target_emotions
    

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
    

    def suggest_promo(self, session, available_promos:dict) -> typing.Optional[str]:
        def promo_filter(p, s):
            # Try-except statement to handle wrong pblished items
            try :
                # Checking status
                if p["currentStatus"].lower()!="active" or (not self.__check_schedule_time(p["startScheduleTime"], p["endScheduleTime"])) or \
                    (not self.__check_date_range(p["startDate"], p["endDate"])):
                    return False
                # Checking age and emotion
                if not self.__check_inference_results(session, p["minAudienceAge"], p["maxAudienceAge"], p["targetEmotions"]):
                    return False
            except:
                return False
            
            return True

        result      = None
        # Filering those that can be used
        f_promos    = list(filter(lambda item : promo_filter(available_promos[item], session), available_promos))
        # Randomly choosing an item
        if len(f_promos)!=0:
            self.__logger.debug(f"Possible promos: {f_promos}")
            random.shuffle(f_promos)
            result  = f_promos[0]
        else:
            self.__logger.debug("No promos available!")

        return result
    

    def suggest_advertisement(self, session, available_advertisements) -> typing.Optional[str]:
        def adv_filter(a, s):
            # Try-except statement to handle wrong pblished items
            try :
                # Checking status
                if a["currentStatus"].lower()!="active" or (not self.__check_schedule_time(a["startScheduleTime"], a["endScheduleTime"])) or \
                    (not self.__check_date_range(a["startDate"], a["endDate"])):
                    return False
                # Checking age and emotion
                if a["targetedAdv"]==True and (not self.__check_inference_results(session, a["minAudienceAge"], a["maxAudienceAge"], a["emotions"])):
                    return False
            except:
                return False
            return True
        
        result  = None
        # Filtering those that can be used
        f_advs  = list(filter(lambda item : adv_filter(available_advertisements[item], session), available_advertisements))
        # Randomly choosing an item
        if len(f_advs)!=0:
            self.__logger.debug(f"Possible advs: {f_advs}")
            random.shuffle(f_advs)
            result  = f_advs[0]
        else:
            self.__logger.debug("No promos available!")

        return result