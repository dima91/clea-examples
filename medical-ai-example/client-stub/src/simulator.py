
import asyncio, random, utils, traceback
from copy import deepcopy
from typing import Tuple
from datetime import datetime, timedelta
from astarte_client import AstarteClient
import utils


class Simulator:

    __config        = None
    __client        = None


    def __init__(self, config, client:AstarteClient) -> None:
        self.__config               = config
        self.__client               = client


    def __get_room_descriptor(self, room_id) -> dict:
        results = list(filter (lambda e: e['id']==room_id, self.__config["rooms"]["descriptors"]))
        if len(results)!=1:
            print(f"DANGEROUS: no or too much room descriptors for {room_id} -> {results}")
            raise Exception()
        return results[0]


    def __is_event_expired(self, now, room_id) -> bool:
        desc            = self.__get_room_descriptor(room_id)
        status_desc     = desc['status']
        end_datetime    = utils.parse_string_datetime(status_desc['start_time'])+timedelta(seconds=status_desc['duration_s'])
        return now>end_datetime


    def __is_hospitalization_over(self, room_id, now:datetime) -> bool:
        release_time    = utils.parse_string_datetime(self.__get_room_descriptor(room_id)["patient_release_date"])
        #print(f"release_time:{release_time}")
        return release_time<now
    

    def __is_in_hospitalization_range(self, now:datetime) -> bool:
        s_time  = utils.parse_string_time(self.__config['rooms']['hospitalization_range_h'][0])
        e_time  = utils.parse_string_time(self.__config['rooms']['hospitalization_range_h'][1])
        return s_time.time() < now.time() < e_time.time()
    

    def __apply_status(self, room_id:int, prev_status:str, curr_status:str, start_time:datetime, duration:int, confidence:int):
        status_desc = self.__get_room_descriptor(room_id)['status']
        status_desc['previous_status']  = prev_status
        status_desc['current_status']   = curr_status
        status_desc['start_time']       = None if start_time==None else utils.format_datetime(start_time)
        status_desc['duration_s']       = duration
        status_desc['confidence']       = confidence


    def __create_patient(self, room_id:int, now:datetime) -> bool:

        if random.random()>self.__config['rooms']['patient_generation_min_probability'] and \
            self.__is_in_hospitalization_range(now):

            h_duration_range    = self.__config["rooms"]["hospitalization_duration_range_d"]
            start_release_t     = utils.parse_string_time(self.__config["rooms"]["release_range_h"][0])
            end_release_t       = utils.parse_string_time(self.__config["rooms"]["release_range_h"][1])
            release_offset_s    = random.randint(0,(end_release_t-start_release_t).total_seconds())
            release_t           = start_release_t+timedelta(seconds=release_offset_s)

            room_desc       = self.__get_room_descriptor(room_id)
            release_date    = now+timedelta(days=random.randint(h_duration_range[0], h_duration_range[1]))
            release_date    = release_date.replace(hour=release_t.hour, minute=release_t.minute, second=0, microsecond=0)

            room_desc['patient_id']                     = random.randint(0, self.__config['rooms']['max_patient_id'])
            room_desc['diagnosis_idx']                  = random.randint(0, len(self.__config['rooms']['diagnoses_list'])-1)
            room_desc['patient_hospitalization_date']   = utils.format_datetime(now)
            room_desc['patient_release_date']           = utils.format_datetime(release_date)

            self.__apply_status(room_id, "NORMAL", "NORMAL", None, None, 1)

            return True
        
        return False
    

    def __move_to_next_status(self, now:datetime, room_id) -> None:
        # Current status differs from NORMAL -> deciding which is the next one
        desc        = self.__get_room_descriptor(room_id)
        curr_status = desc['status']['current_status']
        prev_status = desc['status']['previous_status']

        if curr_status=='WARNING':
            if prev_status=="NORMAL":
                # Can move to ALERT or NORMAL status
                prev_status = curr_status
                curr_status = "ALERT" if random.random() > .5 else "NORMAL"
            elif prev_status=="ALERT":
                # Can move only to NORMAL status
                prev_status = curr_status
                curr_status = "NORMAL"
        elif curr_status=='ALERT':
            # Can move only to WARNING
            prev_status = curr_status
            curr_status = "WARNING"

        
        self.__apply_status(room_id, prev_status, curr_status, now,
                            random.uniform(self.__config['events']['min_event_duration_s'], self.__config['events']['max_event_duration_s']),
                            random.uniform(self.__config['events']['min_confidence'], self.__config['events']['max_confidence']))
    

    def __create_event(self, now:datetime, room_id:int) -> bool:

        desc    = self.__get_room_descriptor(room_id)
        
        # Considering a random delay, the creation probability, and previous status
        events_config       = self.__config['events']
        last_creation_dt    = None if desc["status"]["start_time"]==None else utils.parse_string_datetime(desc["status"]["start_time"])
        min_event_delay     = random.uniform(events_config["min_delay_s"], events_config["max_delay_s"])
        
        if (last_creation_dt==None or (now-last_creation_dt).total_seconds()>min_event_delay) and \
            random.random()<events_config["hourly_probabilities"][str(now.hour)]:
            
            event_name      = "NORMAL"
            while event_name=="NORMAL":
                event_name  = random.choice(list(utils.EventType)).value
            duration        = random.uniform(events_config['min_event_duration_s'], events_config['max_event_duration_s'])
            confidence      = random.uniform(events_config['min_confidence'], events_config['max_confidence'])
            self.__apply_status(room_id, desc["status"]['current_status'], event_name, now, duration, confidence)

            return True

        return False


    async def run(self) -> None:
        try :

            # Setting up rooms...
            loop_delay_s    = self.__config["loop_delay_s"]
            rooms           = []
            for d in self.__config['rooms']['descriptors'] :
                rooms.append(d['id'])
                h_date  = utils.parse_string_datetime(d['patient_hospitalization_date'])
                r_date  = utils.parse_string_datetime(d['patient_release_date'])
                self.__client.publish_room_descriptor(d['id'], d['patient_id'], self.__config['rooms']['diagnoses_list'][d['diagnosis_idx']],
                                                      h_date, r_date)

            # Setting up initial status..
            await asyncio.sleep(2)
            for desc in self.__config['rooms']['descriptors']:
                self.__client.publish_event(utils.EventType(desc['status']['current_status']), desc['status']['confidence'],
                                            None, None, desc['id'])

            await asyncio.sleep(2)
            self.__client.publish_rooms_identifiers(rooms)


            print("Running..")
            while True:
                await asyncio.sleep(loop_delay_s)
                now = datetime.now()

                # Managing patients in rooms
                for desc in self.__config['rooms']["descriptors"]:
                    # Checking if a new patient has to be created
                    if self.__is_hospitalization_over(desc['id'], now):
                        # Trying to create new patient
                        p_result    = self.__create_patient(desc['id'], now)
                        if p_result:
                            print(f"\n##### New patient created #####\n{self.__get_room_descriptor(desc['id'])}\n\n")
                            diagnosis   = self.__config['rooms']['diagnoses_list'][desc['diagnosis_idx']]
                            h_date      = utils.parse_string_datetime(desc['patient_hospitalization_date'])
                            r_date      = utils.parse_string_datetime(desc['patient_release_date'])
                            self.__client.publish_room_descriptor(desc['id'], desc['patient_id'], diagnosis, h_date, r_date)

                    # Managing existing events
                    elif desc['status']['current_status']!="NORMAL" and self.__is_event_expired(now, desc['id']):
                        self.__move_to_next_status(now, desc['id'])
                        print(f"\n##### Event is expired for room {desc['id']} -> moved to next status #####\n{desc}\n\n")
                        self.__client.publish_event(utils.EventType(desc['status']['current_status']), desc['status']['confidence'],
                                                    None, None, desc['id'])

                    # Eventually creating new events
                    elif desc['status']['current_status']=="NORMAL":
                        e_result    = self.__create_event(now, desc['id'])
                        if e_result:
                            print(f"\n##### New event created for room {desc['id']} #####\n{desc}\n\n")
                            self.__client.publish_event(utils.EventType(desc['status']['current_status']), desc['status']['confidence'],
                                                        None, None, desc['id'])


        except Exception as e:
            print (f"[S] Catched this exception: {e}")
            traceback.print_exc()