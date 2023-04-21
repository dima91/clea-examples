
import time, asyncio
from typing import Tuple
from datetime import datetime, timedelta

import utils
from weatherCollector import WeatherCollector


class Simulator:

    __config            = None
    __client            = None
    __weather_collector = None
    __solar_panel       = None


    def __init__(self, config, client, weather_collector:WeatherCollector) -> None:
        self.__config               = config
        self.__client               = client
        self.__weather_collector    = weather_collector
        self.__solar_panel          = {
            "max_current"   : self.__config["SOLAR_PANEL"]["max_current"],
            "max_voltage"   : self.__config["SOLAR_PANEL"]["max_voltage"],
            "max_power"     : self.__config["SOLAR_PANEL"]["max_current"]*self.__config["SOLAR_PANEL"]["max_voltage"]
        }


    def __get_panel_stats(self, actual_panel_power):
        voltage = utils.get_random_value(actual_panel_power/self.__config["SOLAR_PANEL"]["max_current"],
                                                 self.__config["SOLAR_PANEL"]["input_error"])
        current = utils.get_random_value(actual_panel_power/self.__config["SOLAR_PANEL"]["max_voltage"],
                                            self.__config["SOLAR_PANEL"]["input_error"])
        
        return voltage,current


    # TODO Compute the total required power considering board and external appliances
    def __total_load(self) -> float:
        total_load  = self.__config["BOARD"]["required_voltage"]*self.__config["BOARD"]["required_current"]

        return total_load
    
    # TODO Return total current stats considering board and external appliances
    def __get_load_stats(self):
        voltage = self.__config["BOARD"]["required_voltage"]
        current = self.__config["BOARD"]["required_current"]

        return voltage, current
    

    # Updates battery charge basing on load requirements and power provided by panel
    #   Returns current battery stats
    def __update_battery_charge(self, load_requirements:float, panel_power:float) -> Tuple[float, float, float]:
        # Updating battery charge basing on the update_value (in watts)
        battery_config      = self.__config["BATTERY"]
        remaining_charge    = battery_config["max_charge_watts"]*battery_config["curr_charge_percentage"]
        remaining_charge += load_requirements
        remaining_charge += panel_power

        if remaining_charge<=0:
            return 0,0,0

        # Updating current percentage
        battery_config["curr_charge_percentage"]    = remaining_charge/battery_config["max_charge_watts"]

        # Computing charge stats
        charge_delta    = battery_config["max_charge_watts"]-remaining_charge
        delta_factor    = battery_config["charge_percentage_factor"]*charge_delta

        print(f'remaining_charge:{remaining_charge}, charge_delta:{charge_delta}, delta_factor:{delta_factor}')

        voltage = battery_config["max_voltage"]-delta_factor
        current = battery_config["max_current"]*(voltage/battery_config["max_voltage"])

        return remaining_charge,voltage,current


    async def run(self) -> None:
        try :

            ext_sensors_publish_delay   = timedelta(seconds=float(self.__config["external_sensors_publish_delay_s"]))
            stats_publish_delay         = timedelta(seconds=float(self.__config["stats_publish_delay_s"]))

            now                             = datetime.now()
            last_ext_sensors_publish_time   = now
            last_stats_publish_time         = now

            while True:
                await asyncio.sleep(5)
                now                             = datetime.now()

                # Publishing external sensors values
                if (now-last_ext_sensors_publish_time)>ext_sensors_publish_delay:
                    print('Publishing external sensors values..')
                    last_ext_sensors_publish_time   = now
                    self.__client.publish_day_period(self.__weather_collector.current_day_period())
                    self.__client.publish_temperature(self.__weather_collector.current_temperature())
                    self.__client.publish_wind_speed(self.__weather_collector.current_wind_speed())
                    self.__client.publish_reference_current(round(self.__weather_collector.solar_power_to_watts(self.__config["max_reference_solar_power"]),2))

                # Computing generated power by solar panel
                actual_panel_power      = self.__weather_collector.solar_power_to_watts(self.__solar_panel["max_power"])
                remaining_panel_power   = actual_panel_power
                total_load              = self.__total_load()
                if remaining_panel_power>=total_load:
                    # Providing power supply from solar panel
                    print("Power supply from PANEL")
                    remaining_panel_power -= total_load
                    total_load  = 0
                else :
                    # Providing power supply from battery charge
                    print("Power supply from BATTERY")
                    pass

                # Updating battery charge
                remaining_charge,voltage, current   = self.__update_battery_charge(-total_load, remaining_panel_power)
                print (f"{remaining_panel_power}/{actual_panel_power} W goes to battery")

                if remaining_charge<=0:
                    # No data will be published!
                    pass
                elif (now-last_stats_publish_time)>stats_publish_delay:
                    print('Publishing stats values..')
                    last_stats_publish_time = now

                    # Publishing battery, battery and load stats
                    self.__client.publish_battery_stats(voltage, current)

                    voltage,current = self.__get_panel_stats(actual_panel_power)
                    self.__client.publish_panel_stats(voltage, current)
                    
                    voltage,current = self.__get_load_stats()
                    self.__client.publish_load_stats(voltage, current)

                print("=====\n\n")  #FIXME Remove me!


        except Exception as e:
            print (f"[S] Catched this exception: {e}")