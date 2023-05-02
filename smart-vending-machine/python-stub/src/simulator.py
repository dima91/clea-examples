
class Simulator:

    __config    = None
    __client    = None

    def __init__(self, config, astarte_client) -> None:
        
        self.__config   = config
        self.__client   = astarte_client


    async def run(self) -> None:
        print ("Running..")