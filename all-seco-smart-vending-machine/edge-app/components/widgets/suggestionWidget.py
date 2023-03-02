
from utils import commons
from components.widgets.gifPlayerWidget import GifPlayerWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Signal, QTimer, QRect


class SuggestionWidget (QLabel):

    __current_state         = None
    __logger                = None
    __main_window           = None
    __suggestion_text       = None
    __suggestion_content    = None
    ##########
    SelectedProduct         = Signal(str, float)        # product_id, promod_discounr


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
            self.__suggestion_content   = QStackedWidget()
    
        layout                      = QVBoxLayout()
        layout.addWidget(self.__suggestion_text)
        layout.addWidget(self.__suggestion_content)

        self.setLayout(layout)


    def __on_selected_product(self, e):
        # Map selected product with those that have a promo -> retrieve promo_discount
        #FIXME
        promo_discount  = 0
        self.SelectedProduct.emit(e, promo_discount)


    def update_suggested_products(self, session):
        # TODO Basing on current customer_info, let's select tree products consider also promos (ask them to main window)
        # TODO Map promo products to cloned product with different id and price
        #FIXME TEST
        products    = ProductsWidget(self.__main_window, False, False, ["yvvaJi0LNm", "yvvaJi0LNm", "yvvaJi0LNm"], self.__main_window.products_details)
        products.SelectedProduct.connect(self.__on_selected_product)
        commons.remove_and_set_new_shown_widget(self.__suggestion_content, products)
        pass


    def get_main_window(self):
        return self.__main_window