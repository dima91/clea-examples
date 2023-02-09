
import logging

from utils import commons
from components.widgets.videoWidget import VideoWidget
from components.widgets.suggestionWidget import SuggestionWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize, QTimer, Signal


class RecognitionWindow (QWidget):

    ##########


    ##########


    def __init__(self, config, main_window) -> None:
        super().__init__()

        self.__logger   = commons.create_logger(logging, __name__)



        # FIXME REMOVE ME -> TEST
        lbox_layout = QVBoxLayout()
        rbox_layout = QVBoxLayout()
        hbox    = QHBoxLayout()

        lbox_layout.addWidget(VideoWidget())
        lbox_layout.addWidget(SuggestionWidget())
        lbox_layout.addWidget(FooterWidget(config, QSize(50, 50), None))

        rbox_layout.addWidget(ProductsWidget())
        
        hbox.addLayout(lbox_layout)
        hbox.addLayout(rbox_layout)

        self.setLayout(hbox)
