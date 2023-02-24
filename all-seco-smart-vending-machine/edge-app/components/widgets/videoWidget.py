
from utils import commons
from components.videoThread import VideoThread

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QLabel

import cv2 as cv


class VideoWidget (QLabel):

    __BORDER_RADIUS     = 20

    __logger            = None
    __resolution        = None
    __video_thread      = None
    __current_status    = None
    ##########


    def __init__(self, main_window, video_thread:VideoThread) -> None:
        super().__init__()

        config                  = main_window.get_config()

        self.__logger           = commons.create_logger(__name__)
        self.__video_thread     = video_thread
        self.__resolution       = QSize(float(config["app"]["video_resolution_width"]), float(config["app"]["video_resolution_height"]))
        self.__current_status   = main_window.get_current_status()
        video_thread.NewImage.connect (self.__on_new_image)
        main_window.NewStatus.connect(self.__on_main_status_change)
        self.setObjectName("VideoWidget")
        self.setStyleSheet("QLabel#VideoWidget {border-radius: 10px;}")


    def __on_new_image(self, frame, detections):
        for i in range(len(detections)) :
            d   = detections[i]
            cv.rectangle(frame, (d.min.x(), d.min.y()), (d.max.x(), d.max.y()), (255,105,225), 3)
        self.setPixmap(commons.apply_border_radius(commons.cv_img_to_qt_pixmap(frame, self.__resolution), self.__BORDER_RADIUS, self.__resolution))


    def __on_main_status_change(self, new_status, old_status):
        self.__current_status   = new_status