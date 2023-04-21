
import os, json, asyncio, requests, math
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
        time_format = "%Y-%m-%dT%H:%M"
        daily       = self.__last_weather_data["daily"]
        return datetime.strptime(daily["sunrise"][0], time_format),datetime.strptime(daily["sunset"][0], time_format)

    
    def cloud_cover_percentage(self) -> float:
        now = datetime.now()
        return (float(self.__last_weather_data["hourly"]["cloudcover"][now.hour]))/100


    def current_temperature(self) -> float:
        return float(self.__last_weather_data["current_weather"]["temperature"])

    def current_wind_speed(self) -> float:
        speed   = float(self.__last_weather_data["current_weather"]["windspeed"])
        return round(speed, 2)

    def current_day_period(self) -> DayPeriod:
        # Computing day period basing on current time and sunrise and sunset hours
        # sunrise_t, sunset_t = self.__get_sunrise_sunset_times()
        # now                 = datetime.now()

        # if sunrise_t.time() <= now.time() <= sunset_t.time():
        #     return DayPeriod(1)
        # else:
        #     return DayPeriod(0)
        return DayPeriod(self.__last_weather_data["current_weather"]["is_day"])

    def solar_power_to_watts(self, max_power) -> float:
        if self.current_day_period() == DayPeriod.NIGHT:
            print("It's night")
            return 0
        
        # It depends also on day hour respect to sunset and sunrise: sqrt(day_percentage)
        cloud_percentage    = self.cloud_cover_percentage()
        sunrise_t, sunset_t = self.__get_sunrise_sunset_times()
        now                 = datetime.now()

        sunrise_minutes     = (sunrise_t.hour*60)+sunrise_t.minute
        sunset_minutes      = (sunset_t.hour*60)+sunset_t.minute
        solar_minutes       = sunset_minutes-sunrise_minutes
        curr_minutes_norm   = (now.hour*60)+now.minute-sunrise_minutes
        day_percentage      = 1

        if curr_minutes_norm<(solar_minutes/2):
            day_percentage  = curr_minutes_norm/(solar_minutes/2)
        else:
            day_percentage  = 1-((curr_minutes_norm-(solar_minutes/2))/(solar_minutes/2))
        day_percentage  = math.sqrt(day_percentage)
        
        print(f'sunrise_minutes:{sunrise_minutes}, sunset_minutes:{sunset_minutes}, solar_minutes:{solar_minutes}, curr_minutes_norm:{curr_minutes_norm}, cloud_percentage:{cloud_percentage}, day_percentage:{day_percentage}')

        return (max_power-(max_power*cloud_percentage))*day_percentage


    async def run(self) -> None:
        try :
            weather_config  = self.__config["WEATHER_PARAMS"]
            loop_delay      = float(weather_config["loop_delay_s"])


            while True:
                try :
                    now                 = datetime.now()
                    open_meteo_query    = {
                        "latitude"          : weather_config["latitude"],
                        "longitude"         : weather_config["longitude"],
                        "hourly"            : "temperature_2m,cloudcover",
                        "daily"             : "sunrise,sunset",
                        "windspeed_unit"    : "ms",
                        "current_weather"   : True,
                        "forecast_days"     : 1,
                        "timezone"          : os.environ["TZ"]
                    }
                    weather_data        = requests.get("https://api.open-meteo.com/v1/forecast", timeout=loop_delay/2,
                                                       params=open_meteo_query)
                    self.__last_weather_data    = weather_data.json()
                    await asyncio.sleep(loop_delay)

                except requests.exceptions.RequestException as err:
                    print(f"Requests error: {err}")

        except Exception as e:
            print (f"[WC] Catched this exception: {e}")