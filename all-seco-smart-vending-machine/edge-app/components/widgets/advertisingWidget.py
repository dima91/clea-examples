
from utils import commons
from utils.commons import Status

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AdvertisingWidget (QWidget) :

    __main__window      = None
    __logger            = None
    __adv_label         = None
    ##########


    def __init__(self, main_window) -> None:
        super().__init__()

        self.__main__window = main_window
        self.__logger       = commons.create_logger(__name__)
        self.__adv_label    = QLabel()

        vbox    =   QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(commons.h_center_widget(self.__adv_label))
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.__main__window.SessionUpdate.connect(self.on_session_change)


    def on_session_change(self, session):
        if session.current_status == Status.SELECTION:
            print(session.to_dict())
            if session.shown_advertisement_id == None:
                self.__logger.error("SELECTION staus with None adv_id!")
            else:
                # TODO Displaying advertisement
                self.__adv_label.setText(session.shown_advertisement_id)
                pass