
import asyncio
from utils import commons
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from components.astarteClient import AstarteClient
from components.standbyWidget import StandbyWidget
from components.loaderWidget import LoaderWidget


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
    __standby_widget    = None


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

        self.__standby_widget   = StandbyWidget(config, self.screen_sizes)
        self.__standby_widget.stop()

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

        if self.__current_status == commons.Status.INITIALIZING and new_status == commons.Status.STANDBY:
            # Adding and enabling standby widget
            self.__widgets_stack.setCurrentIndex(self.__widgets_stack.addWidget(self.__standby_widget))
            self.__standby_widget.start ()
        
        # TODO Performing something
        # TODO Assigning and notifying the new status

        pass

    def __astarteConnectionStatusChangesHandler (self, new_status) :
        if new_status == True :
            self.__change_status (commons.Status.STANDBY)
        else :
            print ("[FAILURE] Astarte disconnected!")
