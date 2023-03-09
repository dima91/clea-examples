
from utils import commons

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import QRect, Signal, QSize
from PySide6.QtGui import QPixmap, QColor

import requests, validators, os


class ProductCardBox(QWidget):

    __id                = None
    __main_window       = None
    __logger            = None
    __promo_descriptor  = None
    ##########
    SelectedItem    = Signal(str)


    def __init__(self, main_window, id, name, current_price, image_path, ingredients, target_image_size, product_size,
                 promo_descriptor:dict, card_size:QSize) -> None:
        super().__init__()
        
        self.__id               = id
        self.__main_window      = main_window
        self.__logger           = commons.create_logger(__name__)
        self.__promo_descriptor = promo_descriptor
        self.setObjectName("ProductCardBox")

        inner_layout        = QVBoxLayout()
        
        pixmap              = self.__main_window.images_repository.get_pixmap(image_path)
        pixmap_label        = QLabel()
        name_label          = QLabel(name)
        ingredients_label   = QLabel(self.__array_string_to_string(ingredients) if ingredients!=None else ingredients)
        promo_label         = QLabel("" if promo_descriptor==None else "A special discount for you!")
        price_layout        = self._get_price_layout(current_price)

        pixmap_label.setPixmap(commons.resize_image(pixmap, target_image_size))

        pixmap_label.setObjectName("ProductDescItem")
        inner_layout.addLayout(commons.h_center_widget(pixmap_label))
        inner_layout.addStretch(1)
        name_label.setObjectName("ProductDescItem")
        name_label.setStyleSheet("QLabel{font-size:20px;}")
        inner_layout.addLayout(commons.h_center_widget(name_label))
        if ingredients != None:
            ingredients_label.setObjectName("ProductDescItem")
            inner_layout.addLayout(commons.h_center_widget(ingredients_label))
        promo_label.setObjectName("ProductDescItem")
        promo_label.setStyleSheet("QLabel{font-size:12px; color:green}")
        inner_layout.addLayout(commons.h_center_widget(promo_label))
        #price_layout.setObjectName("ProductDescItem")
        inner_layout.addLayout(price_layout)

        root_label      = QLabel()
        root_obj_name   = "product_card_root_label_lg" if product_size == commons.ProductsCardSize.LARGE else "product_card_root_label_sm"
        root_stylesheet = f"QLabel#{root_obj_name}"+ "{border:3px solid green}" if promo_descriptor!=None else ""
        root_label.setObjectName(root_obj_name)
        root_label.setLayout(inner_layout)
        root_label.setStyleSheet (root_stylesheet)
        root_label.adjustSize()
        root_layout = QBoxLayout(QBoxLayout.BottomToTop)
        root_layout.addWidget(root_label)
        
        self.setLayout(root_layout)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor(192,192,192))
        self.shadow.setBlurRadius(50)
        self.shadow.setOffset(5, 5)
        self.setGraphicsEffect(self.shadow)

        self.setMinimumSize(card_size)
        self.adjustSize()


    def _get_price_layout(self, price) -> QHBoxLayout:
        layout              = QHBoxLayout()
        wrong_price_label   = None
        price_label         = QLabel(str(price)+" €")
        price_label.setObjectName("ProductDescItem")

        if self.__promo_descriptor!=None :
            wrong_price_label   = QLabel(str(price)+" €")
            wrong_price_label.setObjectName("ProductDescItem")
            price_label         = QLabel(str(self.__apply_discount(price))+" €")
            price_label.setObjectName("ProductDescItem")

            wrong_price_label.setStyleSheet("QLabel{color:red;}")
            f   = wrong_price_label.font()
            f.setStrikeOut(True)
            wrong_price_label.setFont(f)
        
        layout.addStretch(3)
        if wrong_price_label!=None:
            layout.addWidget(wrong_price_label)
            layout.addStretch(1)
        layout.addWidget(price_label)
        layout.addStretch(3)

        return layout
    

    def __apply_discount(self, price) -> int:
        return price - (price*self.__promo_descriptor["discount"]/100)


    def __array_string_to_string(self, string_array:str):
        result  = ""
        for s in string_array:
            result += f"{s.capitalize()}, "

        return result[:len(result)-2]


    def mousePressEvent(self, ev):
        # Checking product availability
        product_info    = self.__main_window.get_local_db().get_product_info(self.__id)
        if product_info["remainingItems"]>0:
            self.__card_pressed_handler(ev)
        
        return super().mousePressEvent(ev)
        


    def __card_pressed_handler(self, evt):
        self.SelectedItem.emit(self.__id)