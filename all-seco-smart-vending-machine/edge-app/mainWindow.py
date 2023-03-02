
import asyncio, logging
from utils import commons
from utils.commons import Status, CustomerSession
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Signal, QSize, QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from components.vmcInterfaceThread import VmcInterface
from components.astarteClient import AstarteClient
from components.videoThread import VideoThread
from components.widgets.gifPlayerWidget import GifPlayerWidget
from utils.suggestionsStrategies import SuggestionsStrategies
from components.windows.standbyWindow import StandbyWindow
from components.windows.recognitionWindow import RecognitionWindow
from components.windows.suggestionWindow import SuggestionWindow
from components.windows.selectionWindow import SelectionWindow
from components.windows.paymentWindow import PaymentWindow
from components.windows.dispensingWindow import DispensingWindow

from components.windows.videoLoggerWindow import VideoLoggerWindow


class MainWindow (QMainWindow) :
    """
       Main window that allow to handle signals and set other widget's status
    """

    ##########
    ## Members
    ##########
    SessionUpdate   = Signal(CustomerSession)       # This signal notifies

    introspection           = None
    device_setup            = None
    products_details        = None
    advertisements_details  = None
    promos_details          = None
    ##########
    __screen_sizes      = None
    __logger            = None
    __current_session   = None
    __current_status    = None
    __widgets_stack     = None
    __async_loop        = None
    __astarte_client    = None
    __config            = None
    __vmc_interface     = None
    
    ## Widgets
    __video_thread  = None
    __suggester     = None

    ## Windows
    __standby_window        = None
    __recognition_window    = None
    __suggestion_window     = None
    __selection_window      = None

    __video_logger      = None

    __TRANSACTION_ID_LENGHT = 15


    def __init__(self, config, app_loop) -> None:
        super().__init__()

        self.__widgets_stack    = QStackedWidget(self)
        self.__async_loop       = app_loop
        self.__astarte_client   = AstarteClient(config, self.__async_loop)
        self.__config           = config
        self.__current_status   = Status.INITIALIZING

        # Initializing logging
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s : %(name)s.%(funcName)s]  %(message)s')
        self.__logger   = commons.create_logger (__name__)

        # Getting screen sizes
        self.__screen_sizes = QGuiApplication.primaryScreen().geometry().size()
        self.__logger.info (f"Screen (w,h): ({self.__screen_sizes.width()}, {self.__screen_sizes.height()})")

        self.setWindowTitle ("All SECO Smart Vending Machine")
        self.setCentralWidget (self.__widgets_stack)

        # Creating VideoThread
        self.__video_thread = VideoThread(self, config)

        # Creating suggester
        self.__suggester    = SuggestionsStrategies(config)

        # Creating base window
        loader  = GifPlayerWidget(config["loader"]["loader_path"], False)
        loader.restart()
        self.__widgets_stack.setCurrentIndex (self.__widgets_stack.addWidget(loader))

        # AstarteClient signals
        self.__astarte_client.NewConnectionStatus.connect(self.__astarte_connection_status_changes)
        self.__astarte_client.connect_device()

        # VMC interface thread
        self.__vmc_interface    = VmcInterface(self.__config)

        logging.info ("Setup done!")


    ####################
    ## Public methods ##
    
    def get_config(self):
        return self.__config
    
    
    def get_current_session(self) -> CustomerSession :
        return self.__current_session
    

    def screen_sizes_percentage(self, p) -> QSize() :
        #return QSize (int(float(self.__screen_sizes.width)*p), int(floarself.__screen_sizes.height*p))
        return QSize (float(self.__screen_sizes.width())*p, float(self.__screen_sizes.height())*p)


    #####################
    ## Private methods ##

    def __change_status (self, new_status) :
        self.__logger.info (f"Changing status from  {commons.status_to_string(self.__current_status)}  "
                f"to  {commons.status_to_string(new_status)}")

        # Updating current status
        has_error               = False
        old_status              = self.__current_status
        self.__current_status   = new_status


        if old_status == Status.INITIALIZING and self.__current_status == Status.STANDBY:                       # astarte_initialized
            self.__close_current_session_and_start_new_one()
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__standby_window)

        elif old_status == Status.STANDBY and self.__current_status == Status.RECOGNITION:                      # new_person / NewPerson
            self.__current_session.start_time   = commons.ms_timestamp()
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__recognition_window))
            
        elif old_status == Status.RECOGNITION and self.__current_status == Status.STANDBY:                      # escaped_person / EscapedPerson
            self.__close_current_session_and_start_new_one()
            commons.remove_shown_widget(self.__widgets_stack)
        elif old_status == Status.RECOGNITION and self.__current_status == Status.SUGGESTION:                   # new_customer / NewCustomer
            self.__current_session.current_product_tab_id   = self.__recognition_window.get_selected_products_tab()
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__suggestion_window)
        elif old_status == Status.RECOGNITION and self.__current_status == Status.SELECTION :                   # product_selected / ProductSelected
            self.__current_session.current_product_tab_id   = self.__recognition_window.get_selected_products_tab()
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__selection_window)
            
        elif old_status == Status.SUGGESTION and self.__current_status == Status.SELECTION :                    # product_selected / ProductSelected
            self.__current_session.current_product_tab_id   = self.__suggestion_window.get_selected_products_tab()
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__selection_window)
        elif old_status == Status.SUGGESTION and self.__current_status == Status.STANDBY :                      # escaped_customer / EscapedCustomer
            self.__close_current_session_and_start_new_one()
            commons.remove_shown_widget(self.__widgets_stack)
        
        elif old_status == Status.SELECTION and self.__current_status == Status.RECOGNITION :                    # product_rejected / ProductRejected
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__recognition_window)
        elif old_status == Status.SELECTION and self.__current_status == Status.SUGGESTION :                    # product_rejected / ProductRejected
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__suggestion_window)
        elif old_status == Status.SELECTION and self.__current_status == Status.PAYMENT :                       # selection_confirmed / SelectionConfirmed
            # Generating transaction id
            self.__current_session.update_transaction_id(commons.generate_random_id(self.__TRANSACTION_ID_LENGHT))
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__payment_window)
        
        elif old_status == Status.PAYMENT and self.__current_status == Status.DISPENSING :                      # payment_done / PaymentDone
            commons.remove_and_set_new_shown_widget(self.__widgets_stack, self.__dispensing_window)
        
        elif old_status == Status.DISPENSING and self.__current_status == Status.STANDBY :                      # product_dispensed / ProductDispensed
            self.__close_current_session_and_start_new_one()
            commons.remove_shown_widget(self.__widgets_stack)

        else :
            # Incompatible status! Notifying it and reverting 
            oss = commons.status_to_string(old_status)
            nss = commons.status_to_string(self.__current_status)
            self.__logger.error (f"Error handling new status update: cannot find a matching (old_status,new_status) pair -> {oss},{nss}")
            has_error   = True

        # Notifying new status to subscribers if no error
        if not has_error:
            self.__current_session.previous_status  = old_status
            self.__current_session.current_status   = self.__current_status
            self.SessionUpdate.emit(self.__current_session)


    def __create_windows(self) :
        self.__standby_window   = StandbyWindow(self.__config, self, self.__async_loop)
        self.__standby_window.pause()

        # Creating windows
        self.__recognition_window   = RecognitionWindow(self.__config, self, self.__video_thread)
        self.__suggestion_window    = SuggestionWindow(self.__config, self, self.__video_thread)
        self.__selection_window     = SelectionWindow(self.__config, self, self.__video_thread)
        self.__payment_window       = PaymentWindow(self.__config, self, self.__video_thread, self.__vmc_interface)
        self.__dispensing_window    = DispensingWindow(self.__config, self, self.__video_thread, self.__vmc_interface)

        if self.__config["app"].getboolean("show_video_logger") == True:
            self.__video_logger     = VideoLoggerWindow(self.__video_thread, QSize(float(self.__config["app"]["video_resolution_width"]),
                                                        float(self.__config["app"]["video_resolution_height"])))
            self.__video_logger.show()

        # VideoThread signals
        self.__video_thread.NewPerson.connect(self.__on_new_person)
        self.__video_thread.EscapedPerson.connect(self.__on_escaped_person)
        self.__video_thread.NewCustomer.connect(self.__on_new_customer)
        # VideoLoggerWindow signals
        # StandbyWindow signals
        # RecognitionWindow signals
        self.__recognition_window.SelectedProduct.connect(self.__on_selected_product)
        # SuggestionWindow signals
        self.__suggestion_window.EscapedCustomer.connect(self.__on_escaped_customer)
        self.__suggestion_window.SelectedProduct.connect(self.__on_selected_product)
        # SelectionWindow signals
        self.__selection_window.SelectionConfirmed.connect(self.__on_selection_confirmed)
        # PaymentWindow signals
        self.__payment_window.PaymentDone.connect(self.__on_payment_done)
        # DispensingWindow signals
        self.__dispensing_window.Dispensed.connect(self.__on_product_dispensed)


    def __astarte_connection_status_changes (self, new_status) :
        if new_status == True :
            # Retrieving products list and all their information
            self.introspection          = self.__astarte_client.get_introspection()["data"]
            self.device_setup           = self.__astarte_client.get_device_setup()["data"]
            self.products_details       = self.__astarte_client.get_products_details()["data"]
            self.advertisements_details = self.__astarte_client.get_advertisements_details()["data"]
            self.promos_details         = self.__astarte_client.get_promos_details()["data"]

            self.__create_windows()
            self.__vmc_interface.start()
            self.__change_status (Status.STANDBY)
        else :
            print ("[FAILURE] Astarte disconnected!")


    def __close_current_session_and_start_new_one(self):
        if self.__current_session != None:
            # Closing current session
            self.__current_session.close_session()
            self.__send_session_data()
        # Creating a new session
        self.__current_session  = CustomerSession()


    def __send_session_data(self):
        # Sending to Astarte interesting session information
        s   = self.__current_session
        # Sending customer detection
        self.__astarte_client.send_customer_detection(s.end_time-s.start_time, s.inference_results["age"],
                                                      s.inference_results["emotion"], s.shown_advertisement_id)
        # TODO Updating eventually sold product
        # Sending eventually performed transaction
        if s.chosen_product_id != None:
            p_id        = s.chosen_product_id
            p_details   = self.products_details[p_id]
            price       = p_details["currentPrice"] - (p_details["currentPrice"]*s.promo_discount)
            self.__astarte_client.send_transaction(s.chosen_product_id, "NFC", s.transaction_id, p_details["currentCost"],
                                                   price, s.promo_discount!=0, s.is_chosen_product_suggested)
        pass


    ###################
    ## WINDOWS SLOTS ##
    ###################
    
    def __on_new_person(self):
        # Querying to change status into RECOGNITION
        self.__change_status(Status.RECOGNITION)

    def __on_escaped_person(self, frame, detection, customer_info):
        # Querying to change status into STANDBY
        self.__current_session.new_detection(frame, detection, customer_info)
        self.__change_status(Status.STANDBY)

    def __on_new_customer(self, frame, detection, customer_info):
        self.__current_session.new_detection(frame, detection, customer_info)
        self.__change_status(Status.SUGGESTION)
        
    def __on_escaped_customer(self):
        self.__change_status(Status.STANDBY)

    def __on_selected_product(self, prod_id, is_suggested, promo_discount):
        self.__logger.debug(f"Chosen product: {prod_id}\t\tIs suggested: {is_suggested}")
        self.__current_session.update_chosen_product(prod_id, is_suggested, promo_discount)
        self.__current_session.update_shown_advertisement(self.__suggester.suggest_advertisement(self.__current_session, self.advertisements_details))
        self.__change_status(Status.SELECTION)

    def __on_selection_confirmed (self, is_confirmed):
        self.__logger.debug(f"Is selection confirmed? {is_confirmed}")
        if is_confirmed:
            self.__change_status(Status.PAYMENT)
        else:
            self.__change_status(self.__current_session.previous_status)

    def __on_payment_done(self, is_done):
        self.__logger.debug(f"Is payment done? {is_done}")
        if not is_done:
            self.__logger.critical("NFC payment ends with error!")

        self.__change_status(Status.DISPENSING)

    def __on_product_dispensed(self, is_done):
        self.__logger.debug(f"Is {self.products_details[self.__current_session.chosen_product_id]} product dispensed? {is_done}")
        if not is_done:
            self.__logger.critical(f"Product {self.products_details[self.__current_session.chosen_product_id]} not correctly dispensed!")

        self.__change_status(Status.STANDBY)
