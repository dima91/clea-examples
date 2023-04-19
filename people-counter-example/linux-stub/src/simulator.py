
import random, time, asyncio, holidays, json
from datetime import datetime, timedelta

import utils
from astarteClient import AstarteClient


class Simulator:

    __client            = None
    __loop              = None
    __config            = None
    __scene_zones       = None
    __scene_zones_keys  = None
    __is_running        = False
    __update_interval   = 0


    def __init__(self, config, astarte_client:AstarteClient, loop:asyncio.AbstractEventLoop, update_interval_ms:int,
                 scene_zones:dict, country:str) -> None:
        self.__client           = astarte_client
        self.__loop             = loop
        self.__config           = config
        self.__scene_zones      = scene_zones
        self.__scene_zones_keys = []
        self.__update_interval  = float(update_interval_ms/1000)

        self.__holidays         = holidays.country_holidays(country)

        for z in self.__scene_zones:
            zone    = json.loads(self.__scene_zones[z])
            self.__scene_zones_keys.append(zone["zone_name"])


    def __generate_day_params(self, now:datetime):
        curr_people_count   = 0
        
        # Checking if current day is acelebration day in current country
        if now.date() in self.__holidays :
            # Do nothing: today is a celebration day
            pass
        else:
            #print (f"Arg: {self.__config['MAX_PEOPLE_COUNT']}, {self.__config['PEOPLE_DAY_PERCENTAGE'][str(now.weekday())]}")
            curr_people_count   = utils.compute_int_percentage(self.__config["MAX_PEOPLE_COUNT"],
                                                               self.__config["PEOPLE_DAY_PERCENTAGE"][str(now.weekday())])

        print(f"Params for today({now.date()}):\n\tpeople_count:{curr_people_count}\n\n")
        return curr_people_count
    

    # Basing on people on the office and time, computes the probability that a person can enter in the office
    def __allowed_to_enter(self, now:datetime, remaining_people:int) -> float:
        desc        = self.__config["ZONES_DESCRIPTORS"]["Entrance"]
        start_t     = utils.ENTRANCE_PARAMS["GET_START_TIME"](now, self.__config["ENTRANCE_PARAMS"]["START_TIME"])
        end_t       = utils.ENTRANCE_PARAMS["GET_END_TIME"](now, self.__config["ENTRANCE_PARAMS"]["END_TIME"])
        is_among    = start_t <= now <= end_t

        if remaining_people>0 and desc["current_people_count"]<=desc["MAX_PEOPLE_COUNT"] and is_among:
            return random.uniform(0, 1)

        return 0
    

    def __allowed_to_exit(self, now:datetime, remaining_people:int) -> float:
        desc        = self.__config["ZONES_DESCRIPTORS"]["Entrance"]
        start_t     = utils.EXIT_PARAMS["GET_START_TIME"](now, self.__config["EXIT_PARAMS"]["START_TIME"])
        end_t       = utils.EXIT_PARAMS["GET_END_TIME"](now, self.__config["EXIT_PARAMS"]["END_TIME"])
        is_among    = start_t <= now <= end_t

        if remaining_people>0 and desc["current_people_count"]>0 and is_among:
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
    

    def dump(self, now, max_people_count, people_count) -> None:
        print(f"[{now.time()}] -> {people_count}/{max_people_count}")
        for d in self.__config["ZONES_DESCRIPTORS"]:
            desc    = self.__config["ZONES_DESCRIPTORS"][d]
            print(f"\t{d}:{desc['current_people_count']}")
        print ("\n\n")


    async def run(self) -> None:

        if self.__is_running:
            raise ("Simulator is already running!")

        curr_date                   = None
        max_people_count            = 0
        curr_people_count           = 0
        last_entrance_exit_check    = 0
        last_movements_check        = 0

        self.__is_running   = True

        while True:
            time.sleep(self.__update_interval)

            now = datetime.now()
            
            if curr_date==None or curr_date!=now.date():
                # Generating parameters for current day
                last_entrance_exit_check    = now
                last_movements_check        = now
                curr_date                   = now.date()
                max_people_count            = self.__generate_day_params(now)
                curr_people_count           = 0

            if now.timestamp()-last_entrance_exit_check.timestamp()>self.__config["ENTRANCE_EXIT_DELAY_S"]:
                last_entrance_exit_check    = now
                
                # Computing incoming people
                entrance_prob               = self.__allowed_to_enter(now, max_people_count-curr_people_count)
                min_entrance_probability    = utils.ENTRANCE_PARAMS["GET_MIN_PROBABILITY"](now, self.__config["ENTRANCE_PARAMS"], entrance_prob)
                if entrance_prob>min_entrance_probability:
                    print("Putting a person in the Entrance")
                    curr_people_count += 1
                    self.__config["ZONES_DESCRIPTORS"]["Entrance"]["current_people_count"] += 1

                # Computing outcoming people
                exit_prob               = self.__allowed_to_exit(now, curr_people_count)
                min_exit_probability    = utils.EXIT_PARAMS["GET_MIN_PROBABILITY"](now, self.__config["EXIT_PARAMS"], exit_prob)
                if exit_prob>min_exit_probability:
                    print ("Removing a person from the Entrance")
                    curr_people_count -= 1
                    self.__config["ZONES_DESCRIPTORS"]["Entrance"]["current_people_count"] -= 1

            if now.timestamp()-last_movements_check.timestamp()>self.__config["MOVEMENTS_DELAY_S"]:
                last_movements_check    = now

                # Computing movements around the office
                actions = []    # Array item: [source_area, taregt_area]
                for d in self.__config["ZONES_DESCRIPTORS"]:
                    desc    = self.__config["ZONES_DESCRIPTORS"][d]
                    if desc["current_people_count"]>0:
                        exit_probability        = random.uniform(0,1)
                        curr_exit_probabilities = desc["EXIT_PROBABILITIES"][str(now.hour)]
                        min_exit_probability    = random.uniform(curr_exit_probabilities[0], curr_exit_probabilities[1])
                        if exit_probability>min_exit_probability:
                            # A person can exit from current area
                            # Considering weights of connected areas
                            areas_weights   = []
                            for ca in desc["CONNECTED_AREAS"]:
                                factor              = random.uniform(0,1)
                                target_area_weights = self.__config["ZONES_DESCRIPTORS"][ca]["ENTRANCE_WEIGHTS"][str(now.hour)]
                                weight              = random.uniform(target_area_weights[0], target_area_weights[1])
                                areas_weights.append({"target_area":ca, "weight":factor*weight})
                            #print(f"Chosing among {areas_weights}")
                            areas_weights.sort(key=lambda e:e["weight"], reverse=True)
                            #print(f"Chosing among {areas_weights}")
                            target_area = areas_weights[0]["target_area"]
                            actions.append([d, target_area])

                # Applying actions prepared in the previous step
                for a in actions:
                    #print (a)
                    src_desc        = self.__config["ZONES_DESCRIPTORS"][a[0]]
                    dst_desc        = self.__config["ZONES_DESCRIPTORS"][a[1]]
                    
                    if src_desc["current_people_count"]>0:
                        moved_people    = random.randint(1, src_desc["current_people_count"])
                        while dst_desc["MAX_PEOPLE_COUNT"]<dst_desc["current_people_count"]+moved_people:
                            moved_people -= 1
                        #print(f"Moving {moved_people} people from {a[0]} to {a[1]}")
                        src_desc["current_people_count"] -= moved_people
                        dst_desc["current_people_count"] += moved_people


            # Generating detections
            detections  = []
            for d in self.__config["ZONES_DESCRIPTORS"]:
                desc    = self.__config["ZONES_DESCRIPTORS"][d]
                for i in range(0, desc["current_people_count"]):
                    confidence  = random.uniform(self.__config["DETECTION_CONFIDENCE_RANGE"][0], self.__config["DETECTION_CONFIDENCE_RANGE"][1])
                    if confidence>=self.__config["MIN_CONFIDENCE"]:
                        detections.append(self.__build_detection(confidence, d))

            # Publishing detections to Astarte
            self.__client.send_people_count(detections)

            self.dump(now, max_people_count, curr_people_count)