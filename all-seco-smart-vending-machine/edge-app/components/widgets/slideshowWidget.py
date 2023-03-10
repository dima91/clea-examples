
import os, logging, random

from utils import commons

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QPixmap


class SlideshowWidget (QWidget) :

    ##########
    ## Members
    ##########
    __logger            = None
    __curr_image_idx    = 0
    __imgs_str          = None
    __images_repo       = None
    __image_label       = None
    __async_timer       = None
    __target_size       = None
    ##########


    def __init__(self, imgs_repo, URLs_list, target_size, duration_ms) -> None:
        super().__init__()

        self.__logger       = commons.create_logger (__name__)

        self.__async_timer  = QTimer(self)
        self.__async_timer.timeout.connect (self.__on_timer_timeout)
        self.__async_timer.setInterval(duration_ms)
        self.__images_repo  = imgs_repo
        self.__imgs_str     = []
        self.__target_size  = target_size

        # Loading signage images
        for path in URLs_list:
            self.__logger.debug(f"Retrieving {path}")
            self.__imgs_str.append(path)
            self.__images_repo.get_pixmap(path)
        self.__image_label  = QLabel()
        self.__image_label.setObjectName("slideshow_image")
        self.__show_next_image()

        h_layout    = QHBoxLayout()
        v_layout    = QVBoxLayout()
    
        h_layout.addStretch(1)
        h_layout.addWidget(self.__image_label)
        h_layout.addStretch(1)

        v_layout.addStretch(1)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(1)

        self.setLayout(v_layout)


    def __on_timer_timeout (self) -> None:
        self.__show_next_image()


    def __show_next_image (self) -> None:
        self.__curr_image_idx   = (self.__curr_image_idx+1) % len(self.__imgs_str)
        if self.__curr_image_idx == 0:
            random.shuffle(self.__imgs_str)
        #self.__image_label.setPixmap (self.__images[self.__curr_image_idx])
        target_pixmap   = self.__image_preparer(self.__images_repo.get_pixmap(self.__imgs_str[self.__curr_image_idx]))
        self.__image_label.setPixmap (target_pixmap)


    def __image_preparer(self, pixmap:QPixmap):
        return commons.apply_border_radius(commons.resize_image(pixmap, self.__target_size), 15, self.__target_size)


    def start (self) -> None:
        self.__async_timer.start()


    def pause (self) -> None:
        self.__async_timer.stop()