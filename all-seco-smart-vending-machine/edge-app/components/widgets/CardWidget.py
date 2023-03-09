
from utils import commons

from PySide6.QtWidgets import QWidget, QBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QColor


class CardWidget (QWidget):

    __shadow        = None
    ##########
    SelectedCard    = Signal(str)


    def __init__(self, inner_layout, shadow_color:QColor, blur_radius:int, offset:QPoint, class_name, stylesheet_str=None) -> None:
        super().__init__()
        
        root_label  = QLabel()
        if class_name:
            root_label.setObjectName(class_name)
        if stylesheet_str:
            root_label.setStyleSheet(f"QWidget#{class_name}{stylesheet_str}")
        root_label.setLayout(inner_layout)
        root_label.adjustSize()
        root_layout = QBoxLayout(QBoxLayout.BottomToTop)
        root_layout.addWidget(root_label)
        
        self.setLayout(root_layout)

        self.__shadow   = QGraphicsDropShadowEffect()
        self.__shadow.setColor(shadow_color)
        self.__shadow.setBlurRadius(blur_radius)
        self.__shadow.setOffset(offset.x(), offset.y())
        self.setGraphicsEffect(self.__shadow)


    def mousePressEvent(self, ev):
        self.__card_pressed_handler(ev)
        return super().mousePressEvent(ev)


    def __card_pressed_handler(self, evt):
        self.SelectedItem.emit(self.__id)