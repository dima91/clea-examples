
import time, asyncio
from datetime import datetime, timedelta

from weatherCollector import WeatherCollector


class Simulator:

    __config            = None
    __client            = None
    __weather_collector = None


    def __init__(self, config, client, weather_collector:WeatherCollector) -> None:
        self.__config               = config
        self.__client               = client
        self.__weather_collector    = weather_collector


    async def run(self) -> None:
        try :

            ext_sensors_publish_delay   = timedelta(seconds=float(self.__config["external_sensors_publish_delay_s"]))

            now                             = datetime.now()
            last_ext_sensors_publish_time   = now

            while True:
                await asyncio.sleep(5)
                now                             = datetime.now()

                if (now-last_ext_sensors_publish_time)>ext_sensors_publish_delay:
                    last_ext_sensors_publish_time   = now
                    self.__client.publish_day_period(self.__weather_collector.current_day_period())
                    self.__client.publish_temperature(self.__weather_collector.current_temperature())
                    self.__client.publish_wind_speed(self.__weather_collector.current_wind_speed())
                    #self.__client.publish_reference_current(??)     #FIXME
                    self.__client.publish_reference_current(1.5)

        except Exception as e:
            print (f"[S] Catched this exception: {e}")