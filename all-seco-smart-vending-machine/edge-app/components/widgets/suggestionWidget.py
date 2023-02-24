
from utils import commons
from components.widgets.loaderWidget import LoaderWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QTimer, QRect


class SuggestionWidget (QLabel):

    __current_state         = None
    __logger                = None
    __suggestion_text       = None
    __suggestion_content    = None
    ##########


    ##########


    def __init__(self, main_window, target_products) -> None:
        super().__init__()

        self.__logger               = commons.create_logger(__name__)
        self.__main_window          = main_window

        self.__suggestion_text      = QLabel("I suggest you..." if target_products == None else "Based on your current emotion,\nI suggest you...")
        self.__suggestion_text.setObjectName("SuggestionText")
        self.__suggestion_text.setStyleSheet("QLabel {margin-left:10px}")
        if target_products == None :
            self.__suggestion_content   = LoaderWidget(main_window.get_config(), True)
            self.__suggestion_content.start()
        else :
            self.__suggestion_content   = ProductsWidget(self.__main_window)
    
        layout                      = QVBoxLayout()
        layout.addWidget(self.__suggestion_text)
        layout.addWidget(self.__suggestion_content)

        self.setLayout(layout)


    def get_main_window(self):
        return self.__main_window