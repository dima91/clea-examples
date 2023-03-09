
from utils import commons

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize, QTimer, Signal


class ErrorWindow (QWidget):

    __main_window           = None
    __logger                = None
    __error_label           = None
    __visibility_timer      = None
    __visibility_timeout_ms = None
    ##########
    ErrorShown              = Signal()


    def __init__(self, config, main_window) -> None:
        super().__init__()

        self.__logger                   = commons.create_logger(__name__)
        self.__main_window              = main_window
        self.__visibility_timeout_ms    = int(config["error"]["visibility_timeout_ms"])
        self.__error_label              = QLabel(self)
        self.__error_label.setObjectName("ErrorLabel")
        self.__error_label.setStyleSheet("QLabel#ErrorLabel{font-size:28px;}")

        self.setLayout(commons.h_center_widget(self.__error_label))

        main_window.SessionUpdate.connect(self.__on_session_change)


    def __on_session_change(self, session):
        
        if session.current_status == commons.Status.ERROR:
            # Display the error
            self.__logger.debug(f"Displayng this error:\n{session.error_string}")
            self.__error_label.setText(session.error_string)
            # Starting timeout
            self.__visibility_timer = QTimer(self)
            self.__visibility_timer.setSingleShot(True)
            self.__visibility_timer.setInterval(self.__visibility_timeout_ms)
            self.__visibility_timer.timeout.connect(lambda : self.ErrorShown.emit())
            self.__visibility_timer.start()