
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
    screen_sizes    = QSize()
    ##########
    __logger            = None
    __current_status    = None
    __widgets_stack     = None
    __async_loop        = None
    __astarte_client    = None
    
    __video_thread          = None
    __standby_window        = None
    __recognition_window    = None

    __video_logger      = None


    def __init__(self, config, app_loop) -> None:
        super().__init__()

        self.__widgets_stack    = QStackedWidget(self)
        self.__async_loop       = app_loop
        self.__astarte_client   = AstarteClient(config, self.__async_loop)
        self.__current_status   = Status.INITIALIZING

        # Initializing logging
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s : %(name)s.%(funcName)s]  %(message)s')
        self.__logger   = commons.create_logger (logging, __name__)

        # Getting screen sizes
        self.screen_sizes   = QGuiApplication.primaryScreen().geometry().size()
        self.__logger.info (f"Screen (w,h): ({self.screen_sizes.width()}, {self.screen_sizes.height()})")

        self.setWindowTitle ("All SECO Smart Vending Machine")
        self.setCentralWidget (self.__widgets_stack)

        # Creating VideoThread object
        self.__video_thread = VideoThread(self, config)

        # Creating base windows
        loader  = LoaderWidget(config)
        loader.restart()
        self.__widgets_stack.setCurrentIndex (self.__widgets_stack.addWidget(loader))

        self.__standby_window   = StandbyWindow(config, self, self.__async_loop)
        self.__standby_window.pause()

        self.__recognition_window   = RecognitionWindow(config, self)
        self.__suggestion_window    = SuggestionWindow(config, self)

        if bool(config["app"]["show_video_logger"]) == True:
            self.__video_logger     = VideoLoggerWindow(self.__video_thread, QSize(float(config["app"]["video_resolution_width"]),
                                                        float(config["app"]["video_resolution_height"])))
            self.__video_logger.show()

        # AstarteClient signals
        self.__astarte_client.NewConnectionStatus.connect(self.__astarte_connection_status_changes)
        self.__astarte_client.connect_device()
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

        logging.info ("Setup done!")


    ####################
    ## Public methods ##
    
    def get_current_status(self) -> Status :
        return self.__current_status


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
            # Inserting RecognitionWindow on top of the widgets stack
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__recognition_window))
        elif old_status == Status.RECOGNITION and self.__current_status == Status.STANDBY:                      # escaped_person / EscapedPerson
            commons.remove_shown_widget(self.__widgets_stack)
        elif old_status == Status.RECOGNITION and self.__current_status == Status.SUGGESTION:                   # new_customer / NewCustomer
            commons.remove_shown_widget(self.__widgets_stack)
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__suggestion_window))
        #TODO elif old_status == Status.RECOGNITION and self.__current_status == Status.SELECTION :                   # product_selected / ProductSelected
        #TODO elif old_status == Status.SUGGESTION and self.__current_status == Status.SELECTION :                    # product_selected / ProductSelected
        #TODO elif old_status == Status.SELECTION and self.__current_status == Status.SUGGESTION :                    # product_rejected / ProductRejected
        elif old_status == Status.SUGGESTION and self.__current_status == Status.STANDBY :                      # escaped_customer / EscapedCustomer
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


    def __astarte_connection_status_changes (self, new_status) :
        if new_status == True :
            # TODO Retrieve products list and all their information
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
