
from utils import commons
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.selectionWidget import SelectionWidget

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QSize


class SelectionWindow(QWidget):

    __main_window       = None
    __logger            = None
    __stacked_widget    = None
    ##########
    SelectionConfirmed  = Signal(bool)


    def __init__(self, config, main_window, video_thread) -> None:
        super().__init__()

        self.__logger           = commons.create_logger(__name__)
        self.__main_window      = main_window
        self.__stacked_widget   = QStackedWidget()
        # Registering slot for session change
        main_window.SessionUpdate.connect(self.__on_session_change)

        min_w   = self.__main_window.screen_sizes_percentage(.6).width()
        self.__stacked_widget.setMinimumWidth(min_w)
        hbox    = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addWidget(self.__stacked_widget)

        self.setLayout(hbox)


    def __on_session_change(self, session):
        if session.current_status == commons.Status.SELECTION:
            self.__update_shown_product(session)

            


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
        layout.addStretch(1)
        layout.addWidget(FooterWidget(config, QSize(100, 100), None))

        return layout
    

    def __update_shown_product(self, session):
        selection_w = SelectionWidget(self.__main_window, session)
        selection_w.SelectionConfirmed.connect(lambda b: self.SelectionConfirmed.emit(b))
        commons.remove_and_set_new_shown_widget(self.__stacked_widget, selection_w)