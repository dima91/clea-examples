
from utils import commons

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QPixmap, QColor

import requests, validators, os


class ProductCardBox (QWidget):

    __id            = None
    __logger        = None
    ##########
    SelectedItem    = Signal(str)


    def __init__(self, id, name, current_price, image_path, ingredients, target_image_size, product_size) -> None:
        super().__init__()
        
        self.__id           = id
        self.__logger       = commons.create_logger(__name__)
        self.setObjectName("ProductCardBox")

        inner_layout        = QVBoxLayout()
        
        pixmap              = QPixmap()
        pixmap_label        = QLabel()
        name_label          = QLabel(name)
        ingredients_label   = QLabel(str(ingredients))
        price_label         = QLabel(str(current_price)+" €")
        
        # Checking if image_path is an URL or a file
        if validators.url(image_path) and os.path.isfile(image_path) :
            raise Exception(f"{image_path} is a file and a URL")
        if not validators.url(image_path) and not os.path.isfile(image_path) :
            raise Exception(f"{image_path} is neither a file neither a URL")
        
        if validators.url(image_path) :
            pixmap.loadFromData(requests.get(image_path).content)
        else :
            pixmap.load(image_path)

        pixmap_label.setPixmap(commons.resize_image(pixmap, target_image_size))

        pixmap_label.setObjectName("ProductDescItem")
        inner_layout.addLayout(commons.h_center_widget(pixmap_label))
        name_label.setObjectName("ProductDescItem")
        inner_layout.addLayout(commons.h_center_widget(name_label))
        ingredients_label.setObjectName("ProductDescItem")
        inner_layout.addLayout(commons.h_center_widget(ingredients_label))
        price_label.setObjectName("ProductDescItem")
        inner_layout.addLayout(commons.h_center_widget(price_label))

        root_label  = QLabel()
        root_label.setObjectName("product_card_root_label_lg" if product_size == commons.ProductsCardSize.LARGE else "product_card_root_label_sm")
        root_label.setLayout(inner_layout)
        #root_label.setStyleSheet ("QLabel{padding-left:30px; padding-right:30px;}")
        root_label.adjustSize()
        root_layout = QBoxLayout(QBoxLayout.BottomToTop)
        root_layout.addWidget(root_label)
        
        self.setLayout(root_layout)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor(192,192,192))
        self.shadow.setBlurRadius(50)
        self.shadow.setOffset(5, 5)
        self.setGraphicsEffect(self.shadow)

        self.adjustSize()


    def mousePressEvent(self, ev):
        self.__card_pressed_handler(ev)
        return super().mousePressEvent(ev)


    def __card_pressed_handler(self, evt):
        self.SelectedItem.emit(self.__id)