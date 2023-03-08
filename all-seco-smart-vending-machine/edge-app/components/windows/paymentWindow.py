
from utils import commons
from utils.vendtraceMessage import VmcMessageType, VendtraceMessage, PcMessageType
from components.vmcInterfaceThread import VmcInterface
from components.widgets.videoWidget import VideoWidget
from components.widgets.advertisingWidget import AdvertisingWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.gifPlayerWidget import GifPlayerWidget

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QSize, QTimer

# VMC messages
# PC    <-> VMC
# $Wahl  -> 
#        <-  $WA


class PaymentWindow (QWidget):

    __main_window           = None
    __logger                = None
    __is_active             = None
    __vmc_interface         = None
    __stacked_widgets       = None
    __payment_status        = None      # 0:requested, 1:processing, 2:accepted
    __payment_description   = None
    __payed_timer           = None

    __requsted_gif_duration_ms      = None
    __processing_gif_duration_ms    = None
    __accepted_gif_duration_ms      = None

    __emulated_payment_timer        = None
    ##########
    PaymentDone     = Signal(bool)


    def __init__(self, config, main_window, video_thread, vmc_interface:VmcInterface) -> None:
        super().__init__()

        self.__main_window          = main_window
        self.__logger               = commons.create_logger(__name__)
        self.__is_active            = False
        self.__vmc_interface        = vmc_interface
        self.__payment_description  = QLabel("")
        self.__requsted_gif_duration_ms     = int(config['payment']["requsted_gif_duration_ms"])
        self.__processing_gif_duration_ms   = int(config['payment']["processing_gif_duration_ms"])
        self.__accepted_gif_duration_ms     = int(config['payment']["accepted_gif_duration_ms"])
        self.__main_window.SessionUpdate.connect(self.__on_session_change)
        self.__vmc_interface.NewMessage.connect(self.__on_vmc_message)
        self.__payment_description.setObjectName("PaymentDescription")

        self.setLayout(self.__init_ui(config, video_thread))


    def __init_ui(self, config, video_thread):
        r_layout    = QVBoxLayout()
        l_layout    = self.__build_lbox_layout(config, video_thread)
        root_layout = QHBoxLayout()

        min_w                   = self.__main_window.screen_sizes_percentage(.6).width()
        self.__stacked_widgets  = QStackedWidget()
        self.__stacked_widgets.setMinimumWidth(min_w)

        r_layout.addStretch(1)
        r_layout.addWidget(self.__payment_description)
        r_layout.addStretch(4)
        r_layout.addWidget(self.__stacked_widgets)
        r_layout.addStretch(4)

        root_layout.addLayout(l_layout)
        root_layout.addLayout(r_layout)
        
        return root_layout


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


    def __on_session_change(self, session:commons.CustomerSession):
        if session.current_status == commons.Status.PAYMENT:
            self.__is_active        = True
            self.__payment_status   = 0

            if session.connected_dispenser_id == None:
                # Simulating product dispensing
                self.__logger.debug(f"Simulating payment process")
                self.__show_requested_gif()
                self.__emulated_payment_timer   = QTimer(self)
                self.__emulated_payment_timer.setSingleShot(True)
                self.__emulated_payment_timer.setInterval(self.__requsted_gif_duration_ms)
                self.__emulated_payment_timer.timeout.connect(self.__on_emulated_payment_timer_cb)
                self.__emulated_payment_timer.start()
            else :
                # Asking payment to VMC
                self.__logger.debug(f"Asking payment to VMC for product {session.connected_dispenser_id}!!!!\n\n\n")
                self.__vmc_interface.send_message(f"Wahl*{session.connected_dispenser_id}*")
                self.__show_requested_gif()
        else:
            self.__is_active    = False
            if self.__payed_timer:
                self.__payed_timer.stop()


    def __payment_status_to_description(self) -> str:
        text    = ""
        if self.__payment_status==0:
            text    = "Please place the card on the reader to start."
        elif self.__payment_status==1:
            text    = "Processing payment..."
        elif self.__payment_status==2:
            text    = "Authorization granded!"
        else:
            raise Exception(f"Unknown payment status {self.__payment_status}")
        
        return text


    def __on_vmc_message(self, vmc_message:VendtraceMessage) -> None:
        
        self.__logger.debug(f"VMC: {vmc_message.payload_to_string()}")
        internal_msg    = vmc_message.get_message()
        
        if self.__is_active:
            if internal_msg['message_type']==VmcMessageType.WA and internal_msg['status']=="0": # internal_msg['status']=="<prod_id"
                self.__show_processing_gif()
            elif internal_msg['message_type']==VmcMessageType.KREDIT and internal_msg['total']=='100':                  # TODO Don't hardocde the required value!
                self.__show_accepted_gif()
                self.__start_payed_timer()
            elif internal_msg["message_type"]==VmcMessageType.WA and int(internal_msg['status'])>=2:                    # error status
                self.__free_window_resources()
                self.__main_window.get_current_session().set_error_string(f"Cannot dispense product:  {vmc_message.payload_to_string()}")
                self.PaymentDone.emit(False)
            elif internal_msg["message_type"]==VmcMessageType.WAHL and internal_msg['status']=="0" and internal_msg['choice']=="0":     # error status
                self.__free_window_resources()
                self.__main_window.get_current_session().set_error_string(f"Timeout from VMC:  {vmc_message.payload_to_string()}")
                self.PaymentDone.emit(False)


    def __free_window_resources(self):
        self.__clean_widgets_stack()


    def __on_payed_timer_cb(self):
        self.__free_window_resources()
        self.PaymentDone.emit(True)


    def __show_requested_gif(self):
        self.__payment_description.setText(self.__payment_status_to_description())
        payment_gif = GifPlayerWidget(self.__main_window.get_config()["payment"]["requested_gif"], True)
        payment_gif.start()
        commons.remove_and_set_new_shown_widget(self.__stacked_widgets, payment_gif)

    def __show_processing_gif(self):
        self.__payment_description.setText(self.__payment_status_to_description())
        processing_gif  = GifPlayerWidget(self.__main_window.get_config()["payment"]["processing_gif"], True)
        processing_gif.start()
        commons.remove_and_set_new_shown_widget(self.__stacked_widgets, processing_gif)

    def __show_accepted_gif(self):
        self.__payment_description.setText(self.__payment_status_to_description())
        accepted_gif    = GifPlayerWidget(self.__main_window.get_config()["payment"]["accepted_gif"], True)
        accepted_gif.start()
        commons.remove_and_set_new_shown_widget(self.__stacked_widgets, accepted_gif)
        
    def __clean_widgets_stack(self):
        commons.remove_shown_widget(self.__stacked_widgets)
    
    def __start_payed_timer(self):
        # Starting timer to show accepted payment GIF
        self.__payed_timer  = QTimer(self)
        self.__payed_timer.setSingleShot(True)
        self.__payed_timer.setInterval(self.__accepted_gif_duration_ms)
        self.__payed_timer.timeout.connect(self.__on_payed_timer_cb)
        self.__payed_timer.start()

    
    def __on_emulated_payment_timer_cb(self) :
        if self.__payment_status == 0:
            self.__payment_status += 1
            self.__show_processing_gif()
            self.__emulated_payment_timer.start()
        elif self.__payment_status == 1:
            self.__payment_status += 1
            self.__show_accepted_gif()
            self.__start_payed_timer()


# When the payment is successful and the dispense process start, you receive a $WA*1*.... and if it is finished, you
#   receive a $WA*0*.... If there is an error, you can detect it with the status in $WA. $WA*2*... for example is also
#   provided if the dispenser is empty.
        #if content['message_type'] == VmcMessageType.WA and content['status'] == "1":

