
from utils import commons
from utils.commons import Status

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize

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
        self.setLayout(vbox)

        self.__main__window.SessionUpdate.connect(self.on_session_change)


    def on_session_change(self, session):
        if session.current_status == Status.SELECTION:
            if session.shown_advertisement_id == None:
                self.__logger.error("SELECTION staus with None adv_id!")
            else:
                #  Displaying advertisement
                curr_adv    = self.__main__window.advertisements_details[session.shown_advertisement_id]
                #self.__logger.debug(f"Displaying {curr_adv}")
                self.__adv_label.setText(curr_adv["name"])
                pixmap   = QPixmap()
                pixmap.load(curr_adv["imagePath"])
                pixmap      = commons.apply_border_radius(pixmap, 5, pixmap.size())
                app_config  = self.__main__window.get_config()["app"]
                size        = QSize(int(app_config["video_resolution_width"]), int(app_config["video_resolution_height"]))
                self.__adv_label.setPixmap(commons.resize_image(pixmap, size))