
from utils import commons
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal, QSize


class SelectionWindow(QWidget):

    __main_window   = None
    __logger        = None
    ##########


    def __init__(self, config, main_window, video_thread) -> None:
        super().__init__()

        self.__logger       = commons.create_logger(__name__)
        self.__main_window  = main_window
        # Registering slot for session change
        main_window.SessionUpdate.connect(self.__on_session_change)

        hbox    = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addLayout(self.__build_rbox_layout())

        self.setLayout(hbox)


    def __on_session_change(self, session):
        # TODO Implement me
        pass


    def __build_lbox_layout(self, config, video_thread):
        layout  = QVBoxLayout()

        # Video widget
        vw_layout   = QHBoxLayout ()
        vw_layout.addStretch(1)
        vw_layout.addWidget(VideoWidget(self.__main_window, video_thread))
        vw_layout.addStretch(1)
        layout.addLayout(vw_layout)

        # Advertising widget
        advertising_widget  = AdvertisingWidget(self.__main_window)
        layout.addWidget(advertising_widget)
        layout.addWidget(FooterWidget(config, QSize(100, 100), None))

        return layout
    

    def __build_rbox_layout(self):
        vlayout = QVBoxLayout()
        vlayout.addWidget(QPushButton("Super lol"))
        pass