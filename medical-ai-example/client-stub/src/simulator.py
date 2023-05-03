
import asyncio, random, utils
from typing import Tuple
from datetime import datetime, timedelta


class Simulator:

    __config                = None
    __client                = None


    def __init__(self, config, client) -> None:
        self.__config               = config
        self.__client               = client


    async def run(self) -> None:
        try :

            print("Running")
            
            while True:
                await asyncio.sleep(5)
                now = datetime.now()


        except Exception as e:
            print (f"[S] Catched this exception: {e}")