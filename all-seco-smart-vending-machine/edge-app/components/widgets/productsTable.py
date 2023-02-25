
from utils import commons
from components.widgets.productCardWidget import ProductCardBox

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QColor


class ProductsTable (QWidget) :

    __ROWS_COUNT    = 2
    __COLS_COUNT    = 4

    __logger        = None
    __main_window   = None
    ##########
    SelectedProduct = Signal(str)


    def __init__ (self, main_window, prods_id, products_details, products_size) -> None:
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

        # Defining widgets layouts
        v_layout    = QVBoxLayout()
        r0_layout   = QHBoxLayout()     # First row elements
        r1_layout   = QHBoxLayout()     # Second row element

        # Filling first row layout
        for i in range (0, min(self.__COLS_COUNT, len(products))):
            p   = products[i]
            # Create productCardWidget
            card_box    = ProductCardBox(p["ID"], p["name"], p["currentPrice"], p["imagePath"], p["ingredients"], products_image_size, products_size)
            card_box.SelectedItem.connect(self.__on_selected_card)
            r0_layout.addWidget(card_box)

        # Filling second row
        for i in range (0, min(self.__COLS_COUNT, len(products)-self.__COLS_COUNT)):
            p   = products[i+self.__COLS_COUNT]
            # Create productCardWidget
            r1_layout.addWidget(ProductCardBox(p["ID"], p["name"], p["currentPrice"], p["imagePath"], p["ingredients"], products_image_size))


        # Ignoring remaining products!

        # Adding stretches to align item to left
        r0_layout.addStretch(1)
        r1_layout.addStretch(1)
        v_layout.addLayout(r0_layout)
        v_layout.addLayout(r1_layout)
        v_layout.addStretch(1)


        self.adjustSize()

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(10,10,10))
        shadow.setBlurRadius(10)
        shadow.setOffset(5, 5)
        self.setGraphicsEffect(shadow)

        self.setLayout(v_layout)
        self.setStyleSheet("QWidget#ProductsTable {"
                                    "border:10px solid red;"
                                "}")


    def __on_selected_card(self, id):
        self.SelectedProduct.emit(id)

'''
        # Wrapping layout in a root layout
        root_label  = QLabel()
        root_label.setObjectName("productsTable_rootLabel")
        root_label.setLayout(v_layout)
        #root_label.setMinimumWidth(250)
        root_label.adjustSize()
        root_layout = QVBoxLayout()
        root_layout.addWidget(root_label)

        self.setStyleSheet("QWidget#productsTable_rootLabel {"
                                "border:1px solid red;"

                            "}")

        # Adding shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(10,10,10))
        shadow.setBlurRadius(10)
        shadow.setOffset(5, 5)
        self.setGraphicsEffect(shadow)

        self.setLayout(root_layout)
        self.adjustSize()
'''