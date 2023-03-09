
from utils import commons
from components.astarteClient import AstarteClient

from PySide6.QtCore import QObject, QTimer

import random


class DeviceStatisticsGenerator(QObject):
    
    # kWh
    __MIN_POWER_CONSUMPTION         = 2
    __MAX_POWER_CONSUMPTION         = 4
    __POWER_CONSUMPTION_STEP        = .2
    # Celsius
    __MIN_CHAMBER_TEMPERATURE       = 15
    __MAX_CHAMBER_TEMPERATURE       = 32
    __CHAMBER_TEMPERATURE_STEP      = 1
    # kHz
    __MIN_ENGINE_VIBRATION          = 5
    __MAX_ENGINE_VIBRATION          = 15
    __ENGINE_VIBRATION_STEP         = .7

    __main_window                   = None
    __astarte_client:AstarteClient  = None
    __logger                        = None
    __publish_interval              = None
    __timer                         = None

    __current_consumption           = None
    __current_temperature           = None
    __current_vibration             = None
    ##########


    def __init__(self, main_window, astarte_client) -> None:
        super().__init__()

        self.__main_window          = main_window
        self.__astarte_client       = astarte_client
        self.__logger               = commons.create_logger(__name__)
        self.__current_consumption  = (self.__MIN_POWER_CONSUMPTION+self.__MAX_POWER_CONSUMPTION)/2
        self.__current_temperature  = (self.__MIN_CHAMBER_TEMPERATURE+self.__MAX_CHAMBER_TEMPERATURE)/2
        self.__current_vibration    = (self.__MIN_ENGINE_VIBRATION+self.__MAX_ENGINE_VIBRATION)/2
        self.__publish_interval     = int(main_window.get_config()['stats_generator']['publish_interval_ms'])
        self.__timer                = QTimer(self)
        self.__timer.setInterval(self.__publish_interval)
        self.__timer.timeout.connect(self.__on_timeout_cb)
        self.__timer.start()


    def __on_timeout_cb(self):
        #self.__logger.debug ("Sending something..")
        self.__current_temperature  = self.__get_temperature()
        self.__current_consumption  = self.__get_consumption()
        self.__current_vibration    = self.__get_vibration()

        self.__astarte_client.send_device_status(self.__current_consumption, self.__current_temperature, self.__current_vibration)
    

    def __get_consumption(self) -> float:
        res = random.uniform(min(self.__current_consumption+self.__POWER_CONSUMPTION_STEP, self.__MAX_POWER_CONSUMPTION),
                             max(self.__current_consumption-self.__POWER_CONSUMPTION_STEP, self.__MIN_POWER_CONSUMPTION))
        return round(res, 1)


    def __get_temperature(self) -> float:
        res = random.uniform(min(self.__current_temperature+self.__CHAMBER_TEMPERATURE_STEP, self.__MAX_CHAMBER_TEMPERATURE),
                             max(self.__current_temperature-self.__CHAMBER_TEMPERATURE_STEP, self.__MIN_CHAMBER_TEMPERATURE))
        return round(res, 1)
    

    def __get_vibration(self) -> float:
        res = random.uniform(min(self.__current_vibration+self.__ENGINE_VIBRATION_STEP, self.__MAX_ENGINE_VIBRATION),
                             max(self.__current_vibration-self.__ENGINE_VIBRATION_STEP, self.__MIN_ENGINE_VIBRATION))
        return round(res, 1)