
from utils import commons
from components.widgets.gifPlayerWidget import GifPlayerWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, QTimer, QRect


class SuggestionWidget (QLabel):

    __current_state         = None
    __logger                = None
    __suggestion_text       = None
    __suggestion_content    = None
    ##########
    SelectedProduct         = Signal(str)


    def __init__(self, main_window, show_loader) -> None:
        super().__init__()

        self.__logger               = commons.create_logger(__name__)
        self.__main_window          = main_window

        self.__suggestion_text      = QLabel("I suggest you..." if show_loader == True else "Based on your current emotion,\nI suggest you...")
        self.__suggestion_text.setObjectName("SuggestionText")
        self.__suggestion_text.setStyleSheet("QLabel {margin-left:10px}")
        if show_loader == True :
            self.__suggestion_content   = GifPlayerWidget(main_window.get_config()["loader"]["loader_path"], True)
            self.__suggestion_content.start()
        else :
            #FIXME TEST
            self.__suggestion_content   = ProductsWidget(self.__main_window, False, False, ["yvvaJi0LNm", "yvvaJi0LNm", "yvvaJi0LNm"], self.__main_window.products_details)
            #self.__suggestion_content   = ProductsWidget(self.__main_window, False, False, [], {})
            self.__suggestion_content.SelectedProduct.connect(self.__on_selected_product)
    
        layout                      = QVBoxLayout()
        layout.addWidget(self.__suggestion_text)
        layout.addWidget(self.__suggestion_content)

        self.setLayout(layout)


    def __on_selected_product(self, e):
        self.SelectedProduct.emit(e)


    def update_suggested_products(self, session):
        # TODO Basing on current customer_info, let's select tree products
        pass


    def get_main_window(self):
        return self.__main_window