from utils import commons
from utils.vendtraceMessage import VmcMessageType, VendtraceMessage, PcMessageType
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.gifPlayerWidget import GifPlayerWidget

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QSize, QTimer


class DispensingWindow (QWidget):

    __main_window       = None
    __logger            = None
    __is_active         = None
    __vmc_interface     = None
    __stacked_widgets   = None
    __dispensed_timer   = None

    # FIXME TEST memebers
    __test_timer        = None
    __test_timer_status = None
    ##########
    Dispensed     = Signal(bool)


    def __init__(self, config, main_window, video_thread, vmc_interface) -> None:
        super().__init__()

        self.__main_window      = main_window
        self.__logger           = commons.create_logger(__name__)
        self.__is_active        = False
        self.__vmc_interface    = vmc_interface
        self.__main_window.SessionUpdate.connect(self.__on_session_change)
        self.__vmc_interface.NewMessage.connect(self.__on_vmc_message)
        self.setLayout(self.__init_ui(config, video_thread))


    def __init_ui(self, config, video_thread):
        min_w                   = self.__main_window.screen_sizes_percentage(.6).width()
        self.__stacked_widgets  = QStackedWidget()
        self.__stacked_widgets.setMinimumWidth(min_w)
        
        hbox    = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addWidget(self.__stacked_widgets)
        
        return hbox
    
    
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


    def __on_session_change(self, session):
        if session.current_status == commons.Status.DISPENSING:
            self.__is_active    = True
            # TODO Request the payment to the VMC
            payment_gif = GifPlayerWidget(self.__main_window.get_config()["payment"]["processing_gif"], True)
            payment_gif.start()
            self.__stacked_widgets.setCurrentIndex(self.__stacked_widgets.addWidget(payment_gif))

            # FIXME TEST section
            # self.__test_timer_status    = 0
            # self.__test_timer           = QTimer()
            # self.__test_timer.timeout.connect(self.__on_test_timer_cb)
            # self.__test_timer.setInterval(2000)
            # self.__test_timer.start()
        else:
            self.__is_active    = False


    def __on_vmc_message(self, vmc_message):

        if self.__is_active:
            # TODO Do something
            pass