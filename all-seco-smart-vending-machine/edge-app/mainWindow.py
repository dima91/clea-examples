
import asyncio
from utils import commons
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from components.astarteClient import AstarteClient
from components.widgets.loaderWidget import LoaderWidget
from components.windows.standbyWindow import StandbyWindow


class MainWindow (QMainWindow) :
    """
       Main window that allow to handle signals and set other widget's status
    """

    ##########
    ## Members
    ##########
    NewStatus       = Signal(commons.Status)        # This notify when the current status of application changes
    screen_sizes    = QSize()
    ##########
    __current_status    = None
    __widgets_stack     = None
    __async_loop        = None
    __astarte_client    = None
    __standby_window    = None


    def __init__(self, config, app_loop) -> None:
        super().__init__()

        self.__widgets_stack    = QStackedWidget(self)
        self.__async_loop       = app_loop
        self.__astarte_client   = AstarteClient(config, self.__async_loop)
        self.__current_status   = commons.Status.INITIALIZING

        # Getting screen sizes
        self.screen_sizes   = QGuiApplication.primaryScreen().geometry().size()
        print (f"Screen (w,h): ({self.screen_sizes.width()}, {self.screen_sizes.height()})")

        self.setWindowTitle ("All SECO Smart Vending Machine")
        self.setCentralWidget (self.__widgets_stack)

        # Creating base window widgets
        loader  = LoaderWidget(config)
        loader.restart()
        self.__widgets_stack.setCurrentIndex (self.__widgets_stack.addWidget(loader))

        self.__standby_window   = StandbyWindow(config, self.screen_sizes, self.__async_loop)
        self.__standby_window.pause()

        # Registering signals
        self.__astarte_client.NewConnectionStatus.connect (self.__astarteConnectionStatusChangesHandler)


    ####################
    ## Public methods ##
    
    def get_current_status(self) -> commons.Status :
        return self.__current_status


    #####################
    ## Private methods ##

    def __change_status (self, new_status) :
        print (f"[{self.__change_status.__name__}] Changing status from  {commons.status_to_string(self.__current_status)}  "
                f"to  {commons.status_to_string(new_status)}")

        # Updating current status
        old_status              = self.__current_status
        self.__current_status   = new_status

        if old_status == commons.Status.INITIALIZING and self.__current_status == commons.Status.STANDBY:
            # Adding and enabling standby widnows
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__standby_window))
            self.__standby_window.start ()
        #elif
        else :
            # Incompatible status! Notifying it and reverting 
            print (f"[{self.__change_status.__name__}] Error handling new status update!")

        # Notifying new status to subscribers
        self.NewStatus.emit (self.__current_status)
        
        # TODO Performing something


    def __astarteConnectionStatusChangesHandler (self, new_status) :
        # TODO Retrieve products and all their information
        if new_status == True :
            self.__change_status (commons.Status.STANDBY)
        else :
            print ("[FAILURE] Astarte disconnected!")
