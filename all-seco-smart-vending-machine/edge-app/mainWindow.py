
import asyncio
from PyQt6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QGuiApplication
from components.astarteClient import AstarteClient
from components.standbyWindow import StandbyWindow


class MainWindow (QWidget) :
    """
       Main window that allow to handle signals and set other widget's status
    """

    # Defining emitted signals


    def __init__(self, config) -> None:
        super(QWidget, self).__init__()

        self.stack          = QStackedWidget(self)
        self.loop           = asyncio.get_event_loop()
        self.astarte_client = AstarteClient(config, self.loop)

        # TODO Fixing sizes
        #screen_geometry     = QGuiApplication.primaryScreen().geometry()
        #self.screen_width   = screen_geometry.width()
        #self.screen_height  = screen_geometry.height()
        #print (self.screen_height)
        #print (self.screen_width)
        #self.setFixedSize (self.screen_width, self.screen_height-1)

        self.standby_window = StandbyWindow (self)

        #self.stack.setCurrentIndex (self.stack.addWidget(QPushButton('First widget')))  # FIXME test
        #self.stack.setCurrentIndex(self.stack.addWidget(QPushButton('Second widget')))  # FIXME test