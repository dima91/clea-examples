
import time, asyncio
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
        total_load  = self.__config["BOARD"]["required_power"]

        return total_load
    
    # TODO Return total current stats considering board and external appliances
    def __get_load_stats(self):
        voltage = 0
        current = 0

        return voltage, current
    

    def __update_battery_charge(self, update_value:float) -> None:
        # TODO Updating battery charge basing on the update_value (in watts)
        pass

    def __get_battery_stats(Self):
        return 0,0


    async def run(self) -> None:
        try :

            ext_sensors_publish_delay   = timedelta(seconds=float(self.__config["external_sensors_publish_delay_s"]))

            now                             = datetime.now()
            last_ext_sensors_publish_time   = now

            while True:
                await asyncio.sleep(5)
                now                             = datetime.now()

                # Publishing external sensors values
                if (now-last_ext_sensors_publish_time)>ext_sensors_publish_delay:
                    last_ext_sensors_publish_time   = now
                    self.__client.publish_day_period(self.__weather_collector.current_day_period())
                    self.__client.publish_temperature(self.__weather_collector.current_temperature())
                    self.__client.publish_wind_speed(self.__weather_collector.current_wind_speed())
                    self.__client.publish_reference_current(self.__weather_collector.reference_solar_power(self.__solar_panel["max_power"])) # FIXME Pass a different max power

                # Computing generated power by solar panel
                actual_panel_power      = self.__weather_collector.reference_solar_power(self.__solar_panel["max_power"])
                remaining_panel_power   = actual_panel_power
                total_load              = self.__total_load()
                if actual_panel_power>=total_load:
                    # TODO Providing power supply from solar panel
                    remaining_panel_power -= total_load
                else :
                    # TODO Providing power supply from battery charge -> decreasing battery charge!
                    self.__update_battery_charge(-total_load)

                # TODO Remaining power supply goes to battery
                print (f"{remaining_panel_power}W goes to battery")
                self.__update_battery_charge(actual_panel_power)


                # TODO Publishing panel, battery and load stats
                voltage,current = self.__get_panel_stats(actual_panel_power)
                self.__client.publish_panel_stats(voltage, current)
                
                voltage,current = self.__get_battery_stats()
                self.__client.publish_battery_stats(voltage, current)
                
                voltage,current = self.__get_load_stats()
                self.__client.publish_load_stats(voltage, current)


        except Exception as e:
            print (f"[S] Catched this exception: {e}")