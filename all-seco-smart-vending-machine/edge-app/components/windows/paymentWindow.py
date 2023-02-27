
from utils import commons

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal, QSize


class PaymentWindow (QWidget):

    __main_window   = None
    __logger        = None
    __vmc_interface = None
    ##########


    def __init__(self, config, main_window) -> None:
        super().__init__()

        self.__main_window  = main_window
        self.__logger       = commons.create_logger(__name__)
        self.__init_ui()
        self.__main_window.SessionUpdate.connect(self.__on_session_change)


    def __init_ui(self):
        root_layout = QVBoxLayout()
        root_layout.addLayout(commons.h_center_widget(QLabel("PAYING!!!!")))
        
        self.setLayout(root_layout)


    def __on_session_change(self, session):
        pass