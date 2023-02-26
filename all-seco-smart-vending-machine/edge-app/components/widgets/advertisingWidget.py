
from PySide6.QtWidgets import QWidget

class AdvertisingWidget (QWidget) :

    __main__window  = None
    ##########


    def __init__(self, main_window) -> None:
        super().__init__()

        self.__main__window = main_window


    # def new_advertisement(self, session)