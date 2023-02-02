
import asyncio
from utils import commons
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from components.astarteClient import AstarteClient
from components.standbyWidget import StandbyWidget
from components.loaderWidget import LoaderWidget


class MainWindow (QWidget) :
    """
       Main window that allow to handle signals and set other widget's status
    """

    # Defining emitted signals
    NewStatus   = Signal(commons.Status)        # This notify when the current status of application changes


    def __init__(self, config) -> None:
        super(QWidget, self).__init__()

        self.stack          = QStackedWidget(self)
        self.loop           = asyncio.get_event_loop()
        self.astarte_client = AstarteClient(config, self.loop)

        self.current_status = commons.Status.INITIALIZING

        # Getting screen sizes
        screen_geometry     = QGuiApplication.primaryScreen().geometry()
        self.screen_width   = screen_geometry.width()
        self.screen_height  = screen_geometry.height()
        #print (self.screen_height)
        #print (self.screen_width)
        #self.setFixedSize (self.screen_width, self.screen_height-1)

        self.stack.setCurrentIndex (self.stack.addWidget(LoaderWidget (self, config)))

        #self.btn    = QPushButton('First widget')
        #self.btn.setAlignment (Qt.AlignmentFlag.AlignCenter)
        #self.stack.setCurrentIndex (self.stack.addWidget(QPushButton('First widget')))  # FIXME test
        #self.stack.setCurrentIndex(self.stack.addWidget(QPushButton('Second widget')))  # FIXME test