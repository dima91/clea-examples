
from utils import commons
from utils.suggestionsStrategies import SuggestionsStrategies
from components.widgets.gifPlayerWidget import GifPlayerWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Signal, QTimer, QRect

import random


class SuggestionWidget (QLabel):

    __current_state             = None
    __logger                    = None
    __main_window               = None
    __suggester                 = None
    __suggestion_text           = None
    __suggestion_content        = None

    __promo_descriptor          = None
    __promo_product_id          = None
    ##########
    SelectedProduct             = Signal(str, float)        # product_id, promo_discount


    def __init__(self, main_window, show_loader) -> None:
        super().__init__()

        self.__logger               = commons.create_logger(__name__)
        self.__main_window          = main_window

        self.__suggester            = None if show_loader==True else SuggestionsStrategies(main_window.get_config())
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
        # TODO Map selected product with those that have a promo -> retrieve promo_discount
        #FIXME
        promo_discount  = 0
        self.SelectedProduct.emit(e, promo_discount)


    def update_suggested_products(self, session):
        # Collecting suggestions
        suggestions = self.__suggester.suggest_products(session, self.__main_window.products_details)
        print (f"Suggestions are: {suggestions}")
        # Retrieving possible promo
        promo_id                = self.__suggester.suggest_promo(session, self.__main_window.promos_details)
        self.__promo_descriptor = None
        self.__promo_product_id = None
        if promo_id!=None:
            self.__promo_descriptor = self.__main_window.promos_details[promo_id]
            # Chosing the promotional product
            promo_prods             = self.__main_window.promos_details[promo_id]["products"].copy()
            random.shuffle(promo_prods)
            self.__promo_product_id = promo_prods[0]
            self.__logger.debug(f"Chosen promo: {self.__promo_product_id} -> {self.__promo_descriptor['name']}")
            if not self.__promo_product_id in suggestions:
                self.__logger.debug(f"Changing last element of {suggestions}")
                suggestions[len(suggestions)-1] = self.__promo_product_id
            else:
                self.__logger.debug(f"Not needed change of {suggestions}")
            # Moving promotional item to the end
            suggestions.append(suggestions.pop(suggestions.index(self.__promo_product_id)))
        
        self.__logger.debug(f"Final shown products {suggestions}")
        products    = ProductsWidget(self.__main_window, False, False, suggestions, self.__main_window.products_details,
                                     self.__promo_descriptor, self.__promo_product_id)
        products.SelectedProduct.connect(self.__on_selected_product)
        commons.remove_and_set_new_shown_widget(self.__suggestion_content, products)


    def get_main_window(self):
        return self.__main_window