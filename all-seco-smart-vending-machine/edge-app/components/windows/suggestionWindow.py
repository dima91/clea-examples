
from utils import commons
from utils.commons import Status

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QTimer

import logging


class SuggestionWindow (QWidget):

    __logger            = None
    __timer             = None
    __timer_interval    = None
    ##########
    EscapedCustomer = Signal()


    ##########


    def __init__(self, config, main_window) -> None:
        super().__init__()

        self.__logger   = commons.create_logger(logging, __name__)
        # Adding a timeout to came back to standby
        timer_interval  = int(config["ai"]["escaped_customer_threshold_ms"])
        self.__timer    = QTimer()
        self.__timer.timeout.connect (self.__on_escaped_customer_timer_timeout)
        self.__timer.setSingleShot(True)
        self.__timer.setInterval(timer_interval)
        # Registering slot for status change
        main_window.NewStatus.connect(self.__on_main_status_change)


        # FIXME TEST
        vbox    = QVBoxLayout()
        vbox.addWidget (QLabel("suggestionWindow"))
        self.setLayout(vbox)


    def __on_main_status_change(self, new_status, old_status):
        if new_status == Status.SUGGESTION :
            self.__timer.start()
        else :
            self.__timer.stop()


    def __on_escaped_customer_timer_timeout(self) -> None:
        self.EscapedCustomer.emit()