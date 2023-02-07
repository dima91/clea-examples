
import cv2 as cv, numpy as np, pandas, logging, time

from utils import commons
from openvino.inference_engine import IECore

from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import QWidget


class VideoThread (QThread) :

    ## Signals
    NewImage    = Signal (object) # TODO Define signal type
    ## Members
    __logger        = None
    __video_source  = None
    __video_thread  = None
    __freezed_image = None
    __networks      = None


    def __init__(self, main_window, config) -> None:
        super().__init__()

        self.__video_source = cv.VideoCapture(config["app"]["video_source"])
        self.__logger       = commons.create_logger(logging, __name__)
        self.__logger.debug (f'Networks loaded in {self.__load_ai_networks()} seconds')


    def __load_ai_networks(self) -> int:
        start_t = time.time()
        ie      = IECore()
        self.__networks = {
        }
        end_t   = time.time()
        return end_t - start_t


    def run(self):
        try :
            while True:
                pass

        except RuntimeError as re:
            self.__logger.error (f"Catched this error: {re}")


    def start(self):
        # Starting the thread task
        if not self.isRunning():
            super().start()
        else:
            self.__logger.error("Thread already running!")


    def stop(self):
        # TODO Stopping the thread task
        pass


    def get_current_frame(self):
        # TODO Retrieving current (maybe freezed) image
        pass