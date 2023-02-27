
from utils import commons
from utils.commons import Status

from PySide6.QtWidgets import QWidget

class AdvertisingWidget (QWidget) :

    __main__window      = None
    __logger            = None
    __adv_label         = None
    ##########


    def __init__(self, main_window) -> None:
        super().__init__()

        self.__main__window = main_window
        self.__logger       = commons.create_logger(__name__)

        self.__main__window.SessionUpdate.connect(self.on_session_change)


    def on_session_change(self, session):
        if session.current_status == Status.SELECTION:
            #### TODO Choosing the right promo to be shown and updating the __adv_label_image
            self.__logger.debug("Choosing the right advertisement!")
            # TODO Collecting active advertisements
            #advs    = self.__main__window.get_advertisements()
            # TODO Selecting those that can be used
            # TODO Randomly choosing an item
            pass