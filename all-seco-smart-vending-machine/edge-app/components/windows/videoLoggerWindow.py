
import cv2 as cv
from utils import commons
from components.videoThread import VideoThread

from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

# TODO Create and edit a custom qss file to border the images


class VideoLoggerWindow (QWidget) :

    ##########
    __img_label     = None
    __resolution    = None
    ##########
    

    def __init__(self, vt:VideoThread, resolution) -> None:
        super().__init__()

        self.__resolution   = resolution
        self.__img_label    = QLabel(self)
        vbox                = QVBoxLayout()
        vbox.addWidget(self.__img_label)
        self.setLayout(vbox)

        vt.NewImage.connect (self.__on_new_image)


    def __on_new_image(self, frame, detections):
        for i in range(len(detections)) :
            d   = detections[i]
            cv.rectangle(frame, (d.min.x(), d.min.y()), (d.max.x(), d.max.y()), (255,105,225), 3)
        self.__img_label.setPixmap(commons.cv_img_to_qt_pixmap(frame, self.__resolution))