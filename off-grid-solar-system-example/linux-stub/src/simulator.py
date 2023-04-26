
import time, asyncio, random
from typing import Tuple
from datetime import datetime, timedelta

import utils
from weatherCollector import WeatherCollector


class Simulator:

    __config                = None
    __client                = None
    __events_config         = None
    __current_events        = None
    __weather_collector     = None
    __solar_panel_config    = None


    def __init__(self, config, client, weather_collector:WeatherCollector) -> None:
        self.__config               = config
        self.__client               = client
        self.__events_config        = self.__config["EVENTS"]
        self.__current_events       = list()
        self.__weather_collector    = weather_collector
        self.__solar_panel_config   = self.__config["SOLAR_PANEL"]


    def __get_panel_stats(self, actual_panel_power):
        solar_panel_input_err   = self.__solar_panel_config["input_error"]
        voltage                 = utils.get_random_value(self.__solar_panel_config["max_voltage"], solar_panel_input_err)
        # voltage = utils.get_random_value(actual_panel_power/self.__config["SOLAR_PANEL"]["max_current"],
        #                                          self.__config["SOLAR_PANEL"]["input_error"])
        current                 = utils.get_random_value(min(actual_panel_power/voltage, self.__solar_panel_config["max_current"]), solar_panel_input_err)
        
        return voltage,current


    # Compute the total required power considering board and external appliances
    def __total_load(self) -> float:
        total_load  = (self.__config["BOARD"]["required_voltage"]*self.__config["BOARD"]["required_current"])
        
        for evt in self.__current_events:
            actual_voltage  = evt["required_voltage"]
            actual_current  = utils.get_random_value(evt["required_current"], evt["current_error"])
            total_load += (actual_current*actual_voltage)

        return total_load
    
    # Return total current stats considering board and external appliances
    def __get_load_stats(self):
        voltage = self.__config["BOARD"]["required_voltage"]
        current = self.__config["BOARD"]["required_current"]

        for evt in self.__current_events:
            voltage += evt["required_voltage"]
            current += utils.get_random_value(evt["required_current"], evt["current_error"])

        return voltage, current
    

    def __remaining_battery_charge(self) -> float:
        battery_config      = self.__config["BATTERY"]
        return battery_config["max_charge_watts"]*battery_config["curr_charge_percentage"]

    # Updates battery charge basing on load requirements and power provided by panel
    #   Returns current battery stats
    def __update_battery_charge(self, load_requirements:float, panel_power:float) -> Tuple[float, float, float]:
        # Updating battery charge basing on the update_value (in watts)
        battery_config      = self.__config["BATTERY"]
        remaining_charge    = self.__remaining_battery_charge()
        remaining_charge += load_requirements
        remaining_charge += panel_power

        if remaining_charge<=0:
            battery_config["curr_charge_percentage"]    = 0
            return 0,0,0
        elif remaining_charge>battery_config["max_charge_watts"]:
            remaining_charge    = battery_config["max_charge_watts"]

        # Updating current percentage
        battery_config["curr_charge_percentage"]    = remaining_charge/battery_config["max_charge_watts"]

        # Computing charge stats
        charge_delta    = battery_config["max_charge_watts"]-remaining_charge
        delta_factor    = battery_config["charge_percentage_factor"]*charge_delta

        print(f'remaining_charge:{remaining_charge}, charge_delta:{charge_delta}, delta_factor:{delta_factor}')

        voltage = battery_config["max_voltage"]-delta_factor
        current = battery_config["max_current"]*(voltage/battery_config["max_voltage"])

        return remaining_charge,voltage,current


    def __create_event(self) -> dict:
        event_duration_s    = utils.get_random_value(self.__events_config["base_duration_s"], self.__events_config["duration_error"])
        event   = {
            "end_time"          : datetime.now()+timedelta(seconds=event_duration_s),
            "required_voltage"  : 5,
            "voltage_error"     : .02,
            "required_current"  : utils.get_random_value(1.5, 0.5),
            "current_error"     : .02
        }

        return event
    

    def __in_publish_interval(self, now:datetime) -> bool:
        time_format = "%H:%M:%S"
        start       = datetime.strptime(self.__events_config["generation_time_interval"][0], time_format)
        end         = datetime.strptime(self.__events_config["generation_time_interval"][1], time_format)
        return now.time()>=start.time() and now.time()<=end.time()


    async def run(self) -> None:
        try :

            ext_sensors_publish_delay   = timedelta(seconds=float(self.__config["external_sensors_publish_delay_s"]))
            stats_publish_delay         = timedelta(seconds=float(self.__config["stats_publish_delay_s"]))
            events_base_delay           = self.__events_config["base_delay_s"]
            events_delay_error          = self.__events_config["delay_error"]
            max_events_count            = self.__events_config["max_events_count"]

            now                             = datetime.now()
            last_ext_sensors_publish_time   = now
            last_stats_publish_time         = now
            last_event_generation_time      = None

            while True:
                await asyncio.sleep(5)
                now                     = datetime.now()
                print(f"[{now}]")
                #print(f"[{now}] -> _in_publish_interval? {self.__in_publish_interval(now)}")

                if last_event_generation_time==None and self.__in_publish_interval(now):
                    last_event_generation_time  = now
                elif not self.__in_publish_interval(now):
                    last_event_generation_time  = None

                current_day_period      = self.__weather_collector.current_day_period()
                cloud_cover_percentage  = self.__weather_collector.cloud_cover_percentage()
                sunrise_sunset_times    = self.__weather_collector.get_sunrise_sunset_times()
                current_irradiance      = self.__weather_collector.get_current_irradiance()

                # Eventually publishing external sensors values
                if (now-last_ext_sensors_publish_time)>ext_sensors_publish_delay:
                    #print('Publishing external sensors values..')
                    last_ext_sensors_publish_time   = now
                    self.__client.publish_day_period(self.__weather_collector.current_day_period())
                    self.__client.publish_temperature(self.__weather_collector.current_temperature())
                    self.__client.publish_wind_speed(self.__weather_collector.current_wind_speed())
                    self.__client.publish_reference_current(round(utils.solar_power_to_watts(self.__config["reference_solar_panel_size"],
                                                                                                                current_day_period,
                                                                                                                current_irradiance,
                                                                                                                cloud_cover_percentage,
                                                                                                                sunrise_sunset_times),2))

                # Computing generated power by solar panel
                actual_panel_power      = utils.solar_power_to_watts(self.__solar_panel_config["size"], current_day_period,
                                                                     current_irradiance, cloud_cover_percentage, sunrise_sunset_times)
                remaining_panel_power       = actual_panel_power
                curr_power_supply_source    = None
                total_load_power            = self.__total_load()
                if remaining_panel_power>=total_load_power:
                    # Providing power supply from solar panel
                    print("Power supply from PANEL")
                    remaining_panel_power -= total_load_power
                    total_load_power            = 0
                    curr_power_supply_source    = utils.PowerSupplySource.PANEL
                else :
                    # Providing power supply from battery charge
                    print("Power supply from BATTERY")
                    curr_power_supply_source    = utils.PowerSupplySource.BATTERY

                # Updating battery charge
                remaining_charge,voltage, current   = self.__update_battery_charge(-total_load_power, remaining_panel_power)
                print (f"{remaining_panel_power}/{actual_panel_power} W goes to battery")

                load_voltage,load_current       = self.__get_load_stats()
                panel_voltage, panel_current    = self.__get_panel_stats(actual_panel_power)

                if remaining_charge<=0:
                    # No data will be published!
                    print(f'No battery charge! Remaining charge:{self.__remaining_battery_charge()}')
                elif (now-last_stats_publish_time)>stats_publish_delay:
                    #print('Publishing stats values..')
                    last_stats_publish_time = now

                    # Publishing battery, battery and load stats
                    if curr_power_supply_source==utils.PowerSupplySource.PANEL:
                        self.__client.publish_battery_stats(voltage, 0)
                    else:
                        # Applying a percentage to current (battery discharge)
                        discharge_factor    = voltage/self.__config["BATTERY"]["max_voltage"]
                        #print(f"discharge_factor: {discharge_factor} -> {current*discharge_factor}")
                        current             = min(load_current, current*discharge_factor)
                        self.__client.publish_battery_stats(voltage, current)

                    self.__client.publish_panel_stats(voltage, current)
                    self.__client.publish_load_stats(load_voltage, load_current)

                # Checking if there exist ended events
                i   = 0
                while i<len(self.__current_events):
                    evt = self.__current_events[i]
                    if now>evt["end_time"]:
                        del self.__current_events[i]
                        #print(f"Removed event {i} -> {len(self.__current_events)}")
                    else:
                        i+=1

                # Eventually creating an event
                actual_events_delay     = utils.get_random_value(events_base_delay, events_delay_error)
                current_events_count    = len(self.__current_events)
                if last_event_generation_time!=None and \
                   (current_events_count<max_events_count) and \
                   (now-last_event_generation_time).total_seconds()>actual_events_delay and \
                   random.uniform(0,1)>self.__events_config["min_probability"]:
                    
                    last_event_generation_time  = now
                    new_event                   = self.__create_event()
                    print (f"Generated this event:\t{new_event}")
                    self.__current_events.append(new_event)

                print(f"===== {len(self.__current_events)}\n\n")  #FIXME Remove me!


        except Exception as e:
            print (f"[S] Catched this exception: {e}")