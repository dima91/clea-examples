
import random, time
from datetime import datetime


from astarteClient import AstarteClient, ContainerStatus, WaterStatus
from localDB import LocalDB


week_day_presence_percentage   = {
    0   : [.5, .8],     # Monday
    1   : [.75, 1],     # Tuesday
    2   : [.4, .65],    # Wednesday
    3   : [.85, 1],      # Thursday
    4   : [0, .3],      # Friday
    5   : [0, .1],      # Saturday
    6   : [0, 0],       # Sunday
}

coffees_per_hour_percentage     = {
    8   : [.1, .4],
    9   : [.6, .8],
    10  : [.4, .6],
    11  : [0, .2],
    12  : [0, 0],
    13  : [0, 0],
    14  : [.3, .5],
    15  : [.8, 1],
    16  : [0, .2],
    17  : [.4, .6],
    18  : [.1, .3],
    19  : [0, .1],
}

error_solving_delay_m   = [1, 5]


class CoffeeMachineSimulator:

    __client        = None
    __db            = None
    __is_running    = False

    ## .. params
    __PEOPLE_COUNT          = 0
    __CONTAINER_CAPACITY    = 0     # Number of coffees that can be made before the trash container becomes full
    __WATER_CAPACITY        = 0     # Number of coffees that can be made before the water container becomes empty
    __ERROR_SOLVING_DELAY_S = [30, 100]


    def __init__(self, client:AstarteClient, db:LocalDB) -> None:
        self.__client   = client
        self.__db       = db

        d   = datetime.now()
        print(f"\nStarting time is {d.astimezone()}\n\n")

    
    def __compute_int_percentage (self, base_value, factor_range) -> int:
        factor  = random.uniform(factor_range[0], factor_range[1])
        value   = int(round(base_value*factor,0))
        return value


    def __generate_day_params(self, now):
        curr_people_count   = self.__compute_int_percentage(self.__PEOPLE_COUNT, week_day_presence_percentage[now.weekday()])
        coffees_per_hour    = {}
        total_coffees       = 0

        # TODO Checking if it is a celebration day

        for i in coffees_per_hour_percentage:
            coffees_range       = coffees_per_hour_percentage[i]
            coffees_per_hour[i] = self.__compute_int_percentage(curr_people_count, coffees_range)
            if i-1 in coffees_per_hour_percentage  and  coffees_per_hour[i]-coffees_per_hour[i-1]>=0:
                coffees_per_hour[i] -= coffees_per_hour[i-1]

            total_coffees += coffees_per_hour[i]

        print (f"Params for today ({now.date()}) are:\n\tpeople_count: {curr_people_count}\n\tcoffees_per_hour:{coffees_per_hour}\n\ttotal_coffees:{total_coffees}")
        return curr_people_count, coffees_per_hour
    

    def __check_container(self, current_value):
        if current_value==0:
            self.__client.publish_container_status(ContainerStatus.CONTAINER_OPEN_ALARM_EVENT)
            time.sleep(random.randint(self.__ERROR_SOLVING_DELAY_S[0], self.__ERROR_SOLVING_DELAY_S[1]))
            self.__client.publish_container_status(ContainerStatus.CONTAINER_OFF_ALARM_EVENT)
            return self.__CONTAINER_CAPACITY
        
        return current_value
    

    def __check_water(self, current_value):
        if current_value==0:
            self.__client.publish_water_status(WaterStatus.WATER_OPEN_ALARM_EVENT)
            time.sleep(random.randint(self.__ERROR_SOLVING_DELAY_S[0], self.__ERROR_SOLVING_DELAY_S[1]))
            self.__client.publish_water_status(WaterStatus.WATER_OFF_ALARM_EVENT)
            return self.__WATER_CAPACITY
        
        return current_value

    ##############################

    def set_people_count(self, count:int) -> None:
        if not self.__is_running:
            self.__PEOPLE_COUNT = count

    def set_container_capacity(self, capacity:int) -> None:
        if not self.__is_running:
            self.__CONTAINER_CAPACITY   = capacity

    def set_water_capacity(self, capacity:int) -> None:
        if not self.__is_running:
            self.__WATER_CAPACITY   = capacity


    async def run(self) -> None:
        if self.__is_running:
            raise Exception("Simulator is already running")
        
        self.__is_running   = True

        now                             = datetime.now()
        curr_date                       = now.date()
        curr_day_people_count,\
        curr_day_coffees_per_hour       = self.__generate_day_params(now)
        last_iteration_coffees_count    = 0
        remaining_coffees               = self.__CONTAINER_CAPACITY
        remaining_water                 = self.__WATER_CAPACITY

        while True:
            
            # Checking if day changed
            now_date = datetime.now().date()
            if now_date!=curr_date:
                now         = datetime.now()
                curr_date   = now.date()

                # Generating parameters for current day
                curr_day_people_count,\
                curr_day_coffees_per_hour   = self.__generate_day_params(now)

                print (f"Params for {curr_date.date()}")
            
            else :
                # Genrating parameters for current hour
                curr_hour               = datetime.now().hour
                curr_hour_coffees_count = 0
                target_minutes          = []
                try :
                    curr_hour_coffees_count = curr_day_coffees_per_hour[curr_hour]
                    minutes                 = []
                    for i in range(0,59):
                        minutes.append(i)
                    random.shuffle(minutes)
                except KeyError as e:
                    # No coffees should be delivered for this specific hour
                    curr_hour_coffees_count = 0

                while curr_hour_coffees_count>0:
                    target_minutes.append(minutes.pop(0))
                    curr_hour_coffees_count -= 1

                print(f"[{curr_hour}] -> Delivering coffees at minutes {target_minutes}")
                
                # Looping in a certain hour
                while curr_hour==datetime.now().hour:
                    time.sleep(20+random.randint(0,20))
                    
                    print("Checking..")
                    if len(target_minutes)>0 and datetime.now().minute==target_minutes[0]:

                        # Checking if container needs to be emptied
                        remaining_coffees   = self.__check_container(remaining_coffees)
                        # Checking if water needs to be emptied
                        remaining_water     = self.__check_water(remaining_water)

                        # Delivering a coffee
                        if random.randint(0,9)>=7:
                            # Chosen long coffee
                            print(f"Delivering long coffee!")
                            self.__client.send_long_coffee_count(self.__db.new_long_coffee())
                        else:
                            # Chosen short coffee
                            print(f"Delivering short coffee!")
                            self.__client.send_short_coffee_count(self.__db.new_short_coffee())

                        target_minutes.pop(0)
                        remaining_coffees -= 1
                        remaining_water -= 1

                        # Checking if container is full
                        if remaining_coffees == 0:
                            self.__client.publish_container_status(ContainerStatus.CONTAINER_FULL_ALARM_EVENT)
                        # Checking if water is empty
                        if remaining_water == 0:
                            self.__client.publish_water_status(WaterStatus.WATER_EMPTY_ALARM_EVENT)
