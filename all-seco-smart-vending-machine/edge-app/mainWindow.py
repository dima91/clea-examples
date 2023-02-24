
import asyncio, logging
from utils import commons
from utils.commons import Status
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Signal, QSize, QTimer
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from components.astarteClient import AstarteClient
from components.videoThread import VideoThread
from components.widgets.loaderWidget import LoaderWidget
from components.windows.standbyWindow import StandbyWindow
from components.windows.recognitionWindow import RecognitionWindow
from components.windows.suggestionWindow import SuggestionWindow

from components.windows.videoLoggerWindow import VideoLoggerWindow


class MainWindow (QMainWindow) :
    """
       Main window that allow to handle signals and set other widget's status
    """

    ##########
    ## Members
    ##########
                            # new_status        old_status
    NewStatus       = Signal(Status, Status)        # This notify when the current status of application changes

    introspection       = None
    device_setup        = None
    products_details    = None
    ##########
    __screen_sizes      = None
    __logger            = None
    __current_status    = None
    __widgets_stack     = None
    __async_loop        = None
    __astarte_client    = None
    __config            = None
    
    ## Widgets
    __video_thread          = None
    __video_widget          = None
    __products_widget       = None

    ## Windows
    __standby_window        = None
    __recognition_window    = None
    __suggestion_window     = None

    __video_logger      = None


    def __init__(self, config, app_loop) -> None:
        super().__init__()

        self.__widgets_stack    = QStackedWidget(self)
        self.__async_loop       = app_loop
        self.__astarte_client   = AstarteClient(config, self.__async_loop)
        self.__current_status   = Status.INITIALIZING
        self.__config           = config

        # Initializing logging
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s : %(name)s.%(funcName)s]  %(message)s')
        self.__logger   = commons.create_logger (__name__)

        # Getting screen sizes
        self.__screen_sizes = QGuiApplication.primaryScreen().geometry().size()
        self.__logger.info (f"Screen (w,h): ({self.__screen_sizes.width()}, {self.__screen_sizes.height()})")

        self.setWindowTitle ("All SECO Smart Vending Machine")
        self.setCentralWidget (self.__widgets_stack)

        # Creating VideoThread and VideoWidget
        self.__video_thread = VideoThread(self, config)

        # Creating base window
        loader  = LoaderWidget(config, False)
        loader.restart()
        self.__widgets_stack.setCurrentIndex (self.__widgets_stack.addWidget(loader))

        # AstarteClient signals
        self.__astarte_client.NewConnectionStatus.connect(self.__astarte_connection_status_changes)
        self.__astarte_client.connect_device()

        logging.info ("Setup done!")


    ####################
    ## Public methods ##
    
    def get_config(self):
        return self.__config
    
    
    def get_current_status(self) -> Status :
        return self.__current_status
    

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
            # Adding and showing standby widnows
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__standby_window))
        elif old_status == Status.STANDBY and self.__current_status == Status.RECOGNITION:                      # new_person / NewPerson
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__recognition_window))
        elif old_status == Status.RECOGNITION and self.__current_status == Status.STANDBY:                      # escaped_person / EscapedPerson
            self.__suggestion_window.set_selected_products_tab(self.__recognition_window.get_selected_products_tab())
            commons.remove_shown_widget(self.__widgets_stack)
        elif old_status == Status.RECOGNITION and self.__current_status == Status.SUGGESTION:                   # new_customer / NewCustomer
            self.__suggestion_window.set_selected_products_tab(self.__recognition_window.get_selected_products_tab())
            commons.remove_shown_widget(self.__widgets_stack)
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__suggestion_window))
        #TODO elif old_status == Status.RECOGNITION and self.__current_status == Status.SELECTION :                   # product_selected / ProductSelected
            #self.__suggestion_window.set_selected_products_tab(self.__recognition_window.get_selected_products_tab())
        #TODO elif old_status == Status.SUGGESTION and self.__current_status == Status.SELECTION :                    # product_selected / ProductSelected
            #self.__recognition_window.set_selected_products_tab(self.__suggestion_window.get_selected_products_tab())
        #TODO elif old_status == Status.SELECTION and self.__current_status == Status.SUGGESTION :                    # product_rejected / ProductRejected
        elif old_status == Status.SUGGESTION and self.__current_status == Status.STANDBY :                      # escaped_customer / EscapedCustomer
            self.__recognition_window.set_selected_products_tab(self.__suggestion_window.get_selected_products_tab())
            commons.remove_shown_widget(self.__widgets_stack)
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__standby_window))
        #TODO elif old_status == Status.SELECTION and self.__current_status == Status.PAYMENT_REQUESTED :             # selection_confirmed / SelectionConfirmed
        #TODO elif old_status == Status.PAYMENT_REQUESTED and self.__current_status == Status.PAYMENT_ACCEPTED :      # payment_accepted / PaymentAccepted
        #TODO elif old_status == Status.PAYMENT_ACCEPTED and self.__current_status == Status.PAYMENT_PROCESSING :     # TODO
        #TODO elif old_status == Status.PAYMENT_PROCESSING and self.__current_status == Status.DISPENSING :           # payment_done / PaymentDone
        #TODO elif old_status == Status.DISPENSING and self.__current_status == Status.DISPENSED :                    # product_dispensed / ProductDispensed
        #TODO elif old_status == Status.DISPENSED and self.__current_status == Status.STANDBY :                       # reset / Reset
        else :
            # Incompatible status! Notifying it and reverting 
            oss = commons.status_to_string(old_status)
            nss = commons.status_to_string(self.__current_status)
            self.__logger.error (f"Error handling new status update: cannot find a matching (old_status,new_status) pair -> {oss},{nss}")
            has_error   = True

        # Notifying new status to subscribers if no error
        if not has_error:
            self.NewStatus.emit (self.__current_status, old_status)


    def __create_windows(self) :
        self.__standby_window   = StandbyWindow(self.__config, self, self.__async_loop)
        self.__standby_window.pause()

        self.__recognition_window   = RecognitionWindow(self.__config, self, self.__video_thread)
        self.__suggestion_window    = SuggestionWindow(self.__config, self, self.__video_thread)

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
        # SuggestionWindow signals
        self.__suggestion_window.EscapedCustomer.connect(self.__on_escaped_customer)
        # SelectionWindow signals
        # PaymentWindow signals
        # DispensingWindow signals


    def __astarte_connection_status_changes (self, new_status) :
        if new_status == True :
            # Retrieving products list and all their information
            self.introspection      = self.__astarte_client.get_introspection()["data"]
            self.device_setup       = self.__astarte_client.get_device_setup()["data"]
            self.products_details   = self.__astarte_client.get_products_details()["data"]

            self.__create_windows()
            self.__change_status (Status.STANDBY)
        else :
            print ("[FAILURE] Astarte disconnected!")

    
    def __on_new_person(self):
        # Querying to change status into RECOGNITION
        self.__change_status(Status.RECOGNITION)

    def __on_escaped_person(self):
        # Querying to change status into STANDBY
        self.__change_status(Status.STANDBY)

    def __on_new_customer(self, frame, detection, customer_info):
        # Querying to change status into SUGGESION
        self.__change_status(Status.SUGGESTION)
        
    def __on_escaped_customer(self):
        self.__change_status(Status.STANDBY)
