
import time, asyncio


class Simulator:

    __config            = None
    __client            = None
    __weather_collector = None


    def __init__(self, config, client, weather_collector) -> None:
        self.__config               = config
        self.__client               = client
        self.__weather_collector    = weather_collector


    async def run(self) -> None:
        print("Running..")

        while True:
            await asyncio.sleep(1)
            print("[S] Iteration")