
import os
import time
from utils import commons
from components.widgets.footerWidget import FooterWidget
from components.widgets.slideshowWidget import SlideshowWidget

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

# TODO Create and edit a custom qss file to border the images


class StandbyWindow (QWidget) :

    ##########
    ## Members
    ##########
    __signage_slideshow = None
    __icon_size         = QSize(170, 170)
    __images_size       = None


    def __init__(self, config, screen_sizes, async_loop) -> None:
        super().__init__()
        
        self.__images_size          = QSize(screen_sizes.width()*0.8, screen_sizes.height()*0.8)
        self.__signage_slideshow    = SlideshowWidget (config['digital_signage']['base_folder'], self.__images_size,
                                                        int(config['digital_signage']['update_interval_ms']))

        vbox    = QVBoxLayout()
        vbox.addWidget(self.__signage_slideshow)
        vbox.addStretch(1)
        # TODO Create label with correct font size and style
        vbox.addWidget(FooterWidget(config, self.__icon_size, QLabel("Come closer!")))

        self.setLayout(vbox)
        


    def start(self) :
        self.__signage_slideshow.start()


    def pause(self) :
        self.__signage_slideshow.pause()