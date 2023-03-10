
import os
from utils import commons
from components.widgets.footerWidget import FooterWidget
from components.widgets.slideshowWidget import SlideshowWidget

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


class StandbyWindow (QWidget) :

    ##########
    ## Members
    ##########
    __signage_slideshow = None
    __footer_widget     = None
    __icon_size         = QSize(140, 140)
    __images_size       = None


    def __init__(self, config, main_window, async_loop) -> None:
        super().__init__()

        images_list                 = config['digital_signage']['URLs'].split()
        
        self.__images_size          = main_window.screen_sizes_percentage(.83)
        self.__signage_slideshow    = SlideshowWidget (main_window.images_repository, images_list, self.__images_size,
                                                        int(config['digital_signage']['update_interval_ms']))
        self.__footer_widget        = FooterWidget(config, self.__icon_size, "Come closer!")

        # Registering slot to get session changes
        main_window.SessionUpdate.connect(self.__on_session_change)

        vbox    = QVBoxLayout()
        vbox.addWidget(self.__signage_slideshow)
        vbox.addStretch(1)
        vbox.addWidget(self.__footer_widget)

        self.setLayout(vbox)


    def __on_session_change(self, current_session):
        if current_session.current_status == commons.Status.STANDBY:
            self.start()
        else:
            self.pause()



    def start(self) :
        self.__signage_slideshow.start()


    def pause(self) :
        self.__signage_slideshow.pause()