
import asyncio, random, holidays, traceback
from datetime import datetime, timedelta
from typing import Tuple

import utils


class Simulator:

    __config                    = None
    __client                    = None

    def __init__(self, config, astarte_client) -> None:
        
        self.__config                   = config
        self.__client                   = astarte_client


    async def run(self) -> None:
        try:
            print ("Running Simulator loop..")

            loop_delay  = self.__config["loop_delay_s"]

            while True:
                await asyncio.sleep(loop_delay)
                now = datetime.now()


        except Exception as e:
            print("Catched following exception!!")
            traceback.print_exc()