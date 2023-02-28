
from utils import commons
from utils.vendtraceMessage import VmcMessageType, VendtraceMessage, PcMessageType
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.gifPlayerWidget import GifPlayerWidget

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QSize, QTimer


class PaymentWindow (QWidget):

    __main_window       = None
    __logger            = None
    __is_active         = None
    __vmc_interface     = None
    __stacked_widgets   = None
    __payed_timer       = None

    # FIXME TEST memebers
    __test_timer        = None
    __test_timer_status = None
    ##########
    PaymentDone     = Signal(bool)


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
        if session.current_status == commons.Status.PAYMENT:
            self.__is_active    = True
            # TODO Request the payment to the VMC
            payment_gif = GifPlayerWidget(self.__main_window.get_config()["payment"]["requested_gif"], True)
            payment_gif.start()
            self.__stacked_widgets.setCurrentIndex(self.__stacked_widgets.addWidget(payment_gif))

            # FIXME TEST section
            self.__test_timer_status    = 0
            self.__test_timer           = QTimer(self)
            self.__test_timer.setSingleShot(True)
            self.__test_timer.setInterval(500) #FIXME ORIGINAL -> self.__test_timer.setInterval(2000)
            self.__test_timer.timeout.connect(self.__on_test_timer_cb)
            self.__test_timer.start()
        else:
            self.__is_active    = False
            if self.__payed_timer:
                self.__payed_timer.stop()


    def __on_vmc_message(self, vmc_message):

        if self.__is_active:
            ''' TODO Restore me!
            content = vmc_message.get_content()
            self.__logger.log(f"VMC message: {vmc_message.payload_to_string()}")
            '''

            #FIXME TEST section
            if vmc_message == "scanned":
                processing_gif  = GifPlayerWidget(self.__main_window.get_config()["payment"]["processing_gif"], True)
                commons.remove_and_set_new_shown_widget(self.__stacked_widgets, processing_gif)
                processing_gif.start()
            elif vmc_message == "payed":
                accepted_gif    = GifPlayerWidget(self.__main_window.get_config()["payment"]["accepted_gif"], True)
                commons.remove_and_set_new_shown_widget(self.__stacked_widgets, accepted_gif)
                accepted_gif.start()
                # Starting timer to show accepted payment gif for 3 seconds
                # TODO Check if it necessary
                self.__payed_timer  = QTimer(self)
                self.__payed_timer.setSingleShot(True)
                self.__payed_timer.setInterval(500)    # FIXME ORIGINAL -> self.__payed_timer.setInterval(3000)
                self.__payed_timer.timeout.connect(self.__on_payed_timer_cb)
                self.__payed_timer.start()


    def __on_payed_timer_cb(self):
        self.__test_timer.stop()
        self.PaymentDone.emit(True)

    
    def __on_test_timer_cb(self) :
        print ("im into")
        if self.__test_timer_status == 0:
            self.__on_vmc_message("scanned")
            self.__test_timer_status += 1
            self.__test_timer.start()
        elif self.__test_timer_status == 1:
            self.__on_vmc_message("payed")


# When the payment is successful and the dispense process start, you receive a $WA*1*.... and if it is finished, you
#   receive a $WA*0*.... If there is an error, you can detect it with the status in $WA. $WA*2*... for example is also
#   provided if the dispenser is empty.
        #if content['message_type'] == VmcMessageType.WA and content['status'] == "1":

