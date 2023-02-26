
import os
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
    __icon_size         = QSize(140, 140)
    __images_size       = None


    def __init__(self, config, main_window, async_loop) -> None:
        super().__init__()
        
        self.__images_size          = main_window.screen_sizes_percentage(.8)
        self.__signage_slideshow    = SlideshowWidget (config['digital_signage']['base_folder'], self.__images_size,
                                                        int(config['digital_signage']['update_interval_ms']))

        # Registering slot to get session changes
        main_window.SessionUpdate.connect(self.__on_session_change)

        vbox    = QVBoxLayout()
        vbox.addWidget(self.__signage_slideshow)
        vbox.addStretch(1)
        vbox.addWidget(FooterWidget(config, self.__icon_size, "Come closer!"))

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