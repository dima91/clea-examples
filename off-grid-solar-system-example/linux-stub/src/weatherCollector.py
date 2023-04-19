
import time, json, asyncio


class WeatherCollector:

    __config    = None

    def __init__(self, config) -> None:
        self.__config   = config


    async def run(self) -> None:
        while True:
            await asyncio.sleep(.7)
            print("[W] Iteration")