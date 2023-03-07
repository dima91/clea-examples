
from utils import commons
from components.widgets.productCardWidget import ProductCardBox

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QColor


class ProductsTable (QLabel) :

    __ROWS_COUNT    = 2
    __COLS_COUNT    = 4

    __logger        = None
    __main_window   = None
    ##########
    SelectedProduct = Signal(str)


    def __init__ (self, main_window, prods_id, products_details, products_size, promo_descriptor=None, promo_poduct_id=None) -> None:
        super().__init__()

        self.__logger           = commons.create_logger(__name__)
        self.__main_window      = main_window

        self.setObjectName("ProductsTable")
        min_w   = self.__main_window.screen_sizes_percentage(.6).width()
        self.setMinimumWidth(min_w)

        # Building products list
        products    = []
        for id in prods_id:
            products.append(products_details[id])

        prod_conf           = main_window.get_config()['products']
        # products_image_size = QSize(int(prod_conf['image_width']), int(prod_conf['image_height']))
        products_image_size = QSize(int(prod_conf['image_width']), int(prod_conf['image_height'])) if products_size == commons.ProductsCardSize.LARGE \
                                else QSize(int(prod_conf['image_width'])/2, int(prod_conf['image_height'])/2)
        products_card_size  = QSize(int(prod_conf["min_card_width_lg"]), int(prod_conf["min_card_height_lg"])) if products_size == commons.ProductsCardSize.LARGE \
                                    else QSize(int(prod_conf["min_card_width_lg"])/2, int(prod_conf["min_card_height_lg"])/2)

        # Defining widgets layouts
        v_layout    = QVBoxLayout()
        r0_layout   = QHBoxLayout()     # First row elements
        r1_layout   = QHBoxLayout()     # Second row element

        # Filling first row layout
        for i in range (0, min(self.__COLS_COUNT, len(products))):
            p           = products[i]
            apply_promo = (promo_descriptor!=None) and (promo_poduct_id==p["ID"])
            # Create productCardWidget
            card_box    = ProductCardBox(self.__main_window, p["ID"], p["name"], p["currentPrice"], p["imagePath"], p["ingredients"],\
                                         products_image_size, products_size, (promo_descriptor if apply_promo else None), products_card_size)
            card_box.SelectedItem.connect(self.__on_selected_card)
            r0_layout.addWidget(card_box)

        # Filling second row
        for i in range (0, min(self.__COLS_COUNT, len(products)-self.__COLS_COUNT)):
            p           = products[i+self.__COLS_COUNT]
            apply_promo = (promo_descriptor!=None) and (promo_poduct_id==p["ID"])
            # Create productCardWidget
            card_box    = ProductCardBox(self.__main_window, p["ID"], p["name"], p["currentPrice"], p["imagePath"], p["ingredients"],\
                                         products_image_size, products_size, (promo_descriptor if apply_promo else None), products_card_size)
            card_box.SelectedItem.connect(self.__on_selected_card)
            r1_layout.addWidget(card_box)


        # Ignoring remaining products!

        # Adding stretches to align item to left
        r0_layout.addStretch(1)
        r1_layout.addStretch(1)
        v_layout.addLayout(r0_layout)
        v_layout.addLayout(r1_layout)
        v_layout.addStretch(1)


        self.adjustSize()
        self.setLayout(v_layout)


    def __on_selected_card(self, id):
        self.SelectedProduct.emit(id)
