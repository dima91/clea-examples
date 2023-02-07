
import os, logging
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
    __images            = []
    __image_label       = None
    __async_timer       = None
    ##########


    def __init__(self, base_folder, target_size, duration_ms) -> None:
        super().__init__()

        self.__logger       = commons.create_logger (logging, __name__)

        self.__async_timer  = QTimer(self)
        self.__async_timer.timeout.connect (self.__on_timer_timeout)
        self.__async_timer.setInterval(duration_ms)

        # Loading signage images
        for path in os.listdir(base_folder):
            if os.path.isfile(os.path.join(base_folder, path)):
                full_path   = commons.get_abs_path (base_folder, path)
                self.__logger.debug (f"Loading {full_path}")
                tmp_pixmap  = commons.resize_image(QPixmap(full_path), target_size)
                self.__images.append(tmp_pixmap)
        self.__image_label  = QLabel()
        self.__image_label.setPixmap(self.__images[self.__curr_image_idx])

        # TODO Creating central layout
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
        self.__curr_image_idx   = (self.__curr_image_idx+1) % len(self.__images)
        self.__image_label.setPixmap (self.__images[self.__curr_image_idx])


    def start (self) -> None:
        self.__async_timer.start()


    def pause (self) -> None:
        self.__async_timer.stop()