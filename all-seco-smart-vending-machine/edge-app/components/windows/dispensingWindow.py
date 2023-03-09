from utils import commons
from utils.vendtraceMessage import VmcMessageType, VendtraceMessage, PcMessageType
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.dispensingWidget import DispensingWidget, DispensingStatus

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Signal, QSize, QTimer


class DispensingWindow (QWidget):

    __main_window       = None
    __logger            = None
    __is_active         = None
    __vmc_interface     = None
    __top_label         = None
    __dispensing_widget = None
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
        hbox    = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addWidget(self.__build_rbox_widget(config))
        
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
        layout.addStretch(1)
        layout.addWidget(advertising_widget)
        layout.addStretch(1)
        layout.addWidget(FooterWidget(config, QSize(100, 100), None))

        return layout
    

    def __build_rbox_widget(self, config):
        min_w                       = self.__main_window.screen_sizes_percentage(.6).width()
        root_layout                 = QVBoxLayout()
        root_widget                 = QWidget()
        self.__top_label            = QLabel("Wait...")
        cards_width                 = self.__main_window.screen_sizes_percentage(float(config["dispensing"]["card_width_percentage"])).width()
        cards_height                = self.__main_window.screen_sizes_percentage(float(config["dispensing"]["card_height_percentage"])).height()
        self.__dispensing_widget    = DispensingWidget(QSize(cards_width, cards_height), config["dispensing"]["dispensed_img_path"])

        self.__top_label.setObjectName("DispensingLabel")

        self.__dispensing_widget.DispensingUpdate.connect(self.__on_dispensing_widget_update)
        
        root_layout.addWidget(self.__top_label)
        root_layout.addWidget(self.__dispensing_widget)
        
        root_widget.setMinimumWidth(min_w)
        root_widget.setLayout(root_layout)

        return root_widget


    def __on_session_change(self, session):
        if session.current_status == commons.Status.DISPENSING:
            self.__is_active    = True
            # The VMC is dispensing automatically the product
            # Starting dispensing bar
            self.__dispensing_widget.start_dispensing()
        else:
            self.__is_active    = False


    def __on_dispensing_widget_update(self, status:DispensingStatus):
        self.__logger.debug(f"New dispensing widget status: {status}")
        if status == DispensingStatus.STOPPED and self.__is_active:
            self.Dispensed.emit(True)


    def __on_vmc_message(self, vmc_message):

        if self.__is_active:
            # TODO Do something
            pass