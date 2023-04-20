
import time, json, asyncio, requests
from datetime import datetime
from typing import Tuple

from utils import DayPeriod


# Resources
#   https://wttr.in/:help
#   https://github.com/chubin/wttr.in

class WeatherCollector:

    __KMPH_to_MPS       = lambda self,kmph_speed: kmph_speed*0.277778

    __config            = None
    __last_weather_data = None

    def __init__(self, config) -> None:
        self.__config   = config

    
    def __get_sunrise_sunset_times(self) -> Tuple[datetime, datetime]:
        time_format = "%I:%M %p"
        return datetime.strptime(self.__last_weather_data["weather"][0]["astronomy"][0]["sunrise"], time_format),\
                datetime.strptime(self.__last_weather_data["weather"][0]["astronomy"][0]["sunset"], time_format)

    
    def cloud_cover_percentage(self) -> float:
        cloudcover  = float(self.__last_weather_data["current_condition"][0]["cloudcover"])     # FIXME Is 0 the correct index?
        return cloudcover/100


    def current_temperature(self) -> float:
        return float(self.__last_weather_data["current_condition"][0]["temp_C"])

    def current_wind_speed(self) -> float:
        speed   = float(self.__last_weather_data["current_condition"][0]["windspeedKmph"])
        return round(self.__KMPH_to_MPS(speed), 2)

    def current_day_period(self) -> DayPeriod:
        # Computing day period basing on current time and sunrise and sunset hours
        sunrise_t, sunset_t = self.__get_sunrise_sunset_times()
        now                 = datetime.now()

        if sunrise_t.time() <= now.time() <= sunset_t.time():
            return DayPeriod(1)
        else:
            return DayPeriod(0)

    def reference_solar_power(self, max_power) -> float:
        if self.current_day_period() == DayPeriod.NIGHT:
            return 0
        
        # It depends also on day hour respect to sunset and sunrise: sqrt(day_percentage)
        cloud_percentage    = self.cloud_cover_percentage()
        sunrise_t, sunset_t = self.__get_sunrise_sunset_times()
        now                 = datetime.now()

        sunrise_minutes     = (sunrise_t.hour*60)+sunrise_t.minute
        sunset_minutes      = (sunset_t.hour*60)+sunset_t.minute
        solar_minutes       = sunset_minutes-sunrise_minutes
        curr_ref_minutes    = (now.hour*60)+now.minute-sunrise_minutes
        day_percentage      = 1

        if curr_ref_minutes<(solar_minutes/2):
            day_percentage  = curr_ref_minutes/(solar_minutes/2)
        else:
            day_percentage  = (curr_ref_minutes-(solar_minutes/2))/(solar_minutes/2)

        print(f"curr_ref_minutes:{curr_ref_minutes}")
        print(f"solar_minutes:{solar_minutes}")
        print(f"day_percentage:{day_percentage}")

        return max_power*cloud_percentage*day_percentage


    async def run(self) -> None:
        try :
            loop_delay  = float(self.__config["WEATHER_PARAMS"]["loop_delay_s"])
            city        = self.__config["WEATHER_PARAMS"]["city"]

            while True:
                now                         = datetime.now()
                weather_data                = requests.get(f"https://wttr.in/{city}?format=j1")
                self.__last_weather_data    = weather_data.json()
                
                await asyncio.sleep(loop_delay)

        except Exception as e:
            print (f"[WC] Catched this exception: {e}")