
import random, time, asyncio, holidays
from datetime import datetime, timedelta

import utils
from astarteClient import AstarteClient


class Simulator:

    __client            = None
    __loop              = None
    __scene_zones       = None
    __scene_zones_keys  = None
    __is_running        = False
    __update_interval   = 0


    def __init__(self, astarte_client:AstarteClient, loop:asyncio.AbstractEventLoop, update_interval_ms:int,
                 scene_zones:dict, country:str) -> None:
        self.__client           = astarte_client
        self.__loop             = loop
        self.__scene_zones      = scene_zones
        self.__scene_zones_keys = []
        self.__update_interval  = float(update_interval_ms/1000)

        self.__holidays         = holidays.country_holidays(country)

        for z in self.__scene_zones:
            zone    = self.__scene_zones[z]
            self.__scene_zones_keys.append(zone["zone_name"])


    def __compute_int_percentage(self, base_value:int, factor_range:list) -> int:
        curr_factor = random.uniform(factor_range[0], factor_range[1])
        curr_value  = int(round(base_value*curr_factor,0))
        return curr_value


    def __generate_day_params(self, now:datetime):
        curr_people_count   = self.__compute_int_percentage(utils.MAX_PEOPLE_COUNT, utils.PEOPLE_DAY_PERCENTAGE[now.weekday()])

        print(f"Params for today({now.date()}):\n\tpeople_count:{curr_people_count}")
        return curr_people_count
    

    # Basing on people on the office and time, computes the probability that a person can enter in the office
    def __allowed_to_enter(self, now:datetime, remaining_people:int) -> float:
        desc        = utils.ZONES_DESCRIPTORS["Entrance"]
        start_t     = utils.ENTRANCE_PARAMS["GET_START_TIME"](now)
        end_t       = utils.ENTRANCE_PARAMS["GET_END_TIME"](now)
        is_among    = start_t <= now <= end_t

        if remaining_people>0 and desc["current_pople_count"]<=desc["MAX_PEOPLE_COUNT"] and is_among:
            return random.uniform(0, 1)

        return 0
    

    def __allowed_to_exit(self, now:datetime, remaining_people:int) -> float:
        desc        = utils.ZONES_DESCRIPTORS["Entrance"]
        start_t     = utils.EXIT_PARAMS["GET_START_TIME"](now)
        end_t       = utils.EXIT_PARAMS["GET_END_TIME"](now)
        is_among    = start_t <= now <= end_t

        if remaining_people>0 and desc["current_pople_count"]>0 and is_among:
            return random.uniform(0, 1)

        return 0


    def __build_detection(self, confidence:float, zone_name:str) -> dict:
        # ITEM CONTENT:
        #   id              # person ID
        #   conf            # confidence
        #   pos_zone
        #       id          # zone ID   -> index of scene_zones
        #       name        # zone name

        zone_id     = self.__scene_zones_keys.index(zone_name)
        detection   = {
            "id"        : -1,
            "conf"      : confidence,
            "pos_zone"  : {
                    "id"    : zone_id,
                    "name"  : zone_name
            }
        }

        return detection
    

    def dump(self, now) -> None:
        print(f"\n\n[{now.time()}]\n\tEntrance:{utils.ZONES_DESCRIPTORS['Entrance']['current_pople_count']}")
              #f"\n\tBreak Area:{utils.ZONES_DESCRIPTORS['Break Area']['current_pople_count']}")


    async def run(self) -> None:

        if self.__is_running:
            raise ("Simulator is already running!")

        curr_date                   = None
        max_people_count            = 0
        curr_people_count           = 0
        last_entrance_exit_check    = 0

        self.__is_running   = True

        while True:
            time.sleep(self.__update_interval)

            now = datetime.now()
            # FIXME Test section -> TODO Delete me!
            now = now - timedelta(hours=2)
            # FIXME End of test section
            if curr_date==None or curr_date!=now.date():
                # Generating parameters for current day
                last_entrance_exit_check    = now
                curr_date                   = now.date()
                max_people_count            = self.__generate_day_params(now)
                curr_people_count           = 0

                utils.ENTRANCE_PARAMS["current_probability"]    = 0
                utils.EXIT_PARAMS["current_probability"]        = 0

            if now.timestamp()-last_entrance_exit_check.timestamp()>utils.ENTRANCE_EXIT_DELAY_S:
                last_entrance_exit_check    = now
                
                # Computing incoming people
                entrance_prob   = self.__allowed_to_enter(now, max_people_count-curr_people_count)
                if entrance_prob>utils.ENTRANCE_PARAMS["GET_MIN_PROBABILITY"](now):
                    print("Putting a person in the Entrance")
                    utils.ZONES_DESCRIPTORS["Entrance"]["current_pople_count"] += 1

                # Computing outcoming people
                exit_prob   = self.__allowed_to_exit(now, curr_people_count)
                if exit_prob>utils.EXIT_PARAMS["GET_MIN_PROBABILITY"](now):
                    print ("Removing a person from the Entrance")
                    utils.ZONES_DESCRIPTORS["Entrance"]["current_pople_count"] -= 1

            # TODO Computing movements around the office

            # TODO Generating detections
            detections  = []
            #detections.append(self.__build_detection(??, ??))

            # Publishing detections to Astarte
            self.__client.send_people_count(detections)

            self.dump(now)