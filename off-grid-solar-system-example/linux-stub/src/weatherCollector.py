
import enum, time, json, asyncio, requests
from datetime import datetime

from utils import DayPeriod


# Resources
#   https://wttr.in/:help
#   https://github.com/chubin/wttr.in

class WeatherCollector:

    __KMPH_to_MPS       = lambda self,kmph_speed: kmph_speed*0.277778
    __MAX_SOLAR_POWER   = 36    # Watts

    __config            = None
    __last_weather_data = None

    def __init__(self, config) -> None:
        self.__config   = config


    def __hour_to_wttr_weather_data_index(self, now:datetime) -> int:
        return (now.hour//3)

    
    def cloud_cover_percentage(self) -> float:
        return self.__last_weather_data["current_condition"]["cloudcover"]/100


    def current_temperature(self) -> float:
        idx     = self.__hour_to_wttr_weather_data_index(datetime.now())
        return self.__last_weather_data["current_condition"]["tempC"]

    def current_wind_speed(self) -> float:
        speed   = float(self.__last_weather_data["current_condition"]["windspeedKmph"])
        return round(self.__KMPH_to_MPS(speed), 2)

    def current_day_period(self) -> DayPeriod:
        # Computing day period basing on current time and sunrise and sunset hours
        sunrise_str = self.__last_weather_data["weather"][0]["astronomy"][0]["sunrise"]     # FIXME Is 0 the correct index?
        sunset_str  = self.__last_weather_data["weather"][0]["astronomy"][0]["sunset"]      # FIXME Is 0 the correct index?

        time_format = "%I:%M %p"
        sunrise_t   = datetime.strptime(sunrise_str, time_format)
        sunset_t    = datetime.strptime(sunset_str, time_format)
        now         = datetime.now()

        if sunrise_t.time() <= now.time() <= sunset_t.time():
            return DayPeriod(1)
        else:
            return DayPeriod(0)
        
    def reference_solar_power(self, max_power) -> float:
        return max_power*self.cloud_cover_percentage()


    async def run(self) -> None:
        try :
            loop_delay  = float(self.__config["WEATHER_PARAMS"]["loop_delay_s"])
            city        = self.__config["WEATHER_PARAMS"]["city"]

            while True:
                await asyncio.sleep(loop_delay)
                now = datetime.now()

                weather_data                = requests.get(f"https://wttr.in/{city}?format=j1")
                self.__last_weather_data    = weather_data.json()

        except Exception as e:
            print (f"[WC] Catched this exception: {e}")