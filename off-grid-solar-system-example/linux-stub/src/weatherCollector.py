
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

    
    def get_sunrise_sunset_times(self) -> Tuple[datetime, datetime]:
        time_format = "%Y-%m-%dT%H:%M"
        daily       = self.__last_weather_data["daily"]
        return datetime.strptime(daily["sunrise"][0], time_format),datetime.strptime(daily["sunset"][0], time_format)

    
    def cloud_cover_percentage(self) -> float:
        now = datetime.now()
        return (float(self.__last_weather_data["hourly"]["cloudcover"][now.hour]))/100


    def get_current_irradiance(self) -> float:
        now = datetime.now()
        return (float(self.__last_weather_data["hourly"]["direct_radiation_instant"][now.hour]))
        
        
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
                        "hourly"            : "temperature_2m,cloudcover,shortwave_radiation_instant,direct_radiation_instant,"\
                                                "diffuse_radiation_instant,direct_normal_irradiance_instant,terrestrial_radiation_instant",
                        "daily"             : "sunrise,sunset",
                        "windspeed_unit"    : "ms",
                        "current_weather"   : True,
                        "forecast_days"     : 1,
                        "timezone"          : os.environ["TZ"]
                    }
                    weather_data        = requests.get("https://api.open-meteo.com/v1/forecast", timeout=loop_delay/2,
                                                       params=open_meteo_query)
                    #print(f"URL: {weather_data.url}")
                    self.__last_weather_data    = weather_data.json()
                    await asyncio.sleep(loop_delay)

                except requests.exceptions.RequestException as err:
                    print(f"Requests error: {err}")

        except Exception as e:
            print (f"[WC] Catched this exception: {e}")