
import logging

from utils import commons
from components.widgets.videoWidget import VideoWidget
from components.widgets.suggestionWidget import SuggestionWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QSize, QTimer, Signal


class RecognitionWindow (QWidget):

    __main_window       = None
    __logger            = None
    __products_widget   = None
    ##########


    ##########


    def __init__(self, config, main_window, video_thread) -> None:
        super().__init__()

        self.__logger       = commons.create_logger(__name__)
        self.__main_window  = main_window
        
        hbox        = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addLayout(self.__build_rbox_layout())

        self.setLayout(hbox)


    def __build_lbox_layout(self, config, video_thread) -> QVBoxLayout:
        layout  = QVBoxLayout()

        # Video widget
        vw_layout   = QHBoxLayout ()
        vw_layout.addStretch(1)
        vw_layout.addWidget(VideoWidget(self.__main_window, video_thread))
        vw_layout.addStretch(1)
        layout.addLayout(vw_layout)

        # Suggestion widget
        layout.addWidget(SuggestionWidget(self.__main_window, None))
        #layout.addStretch(1)
        layout.addWidget(FooterWidget(config, QSize(100, 100), None))

        return layout
    

    def __build_rbox_layout(self) -> QVBoxLayout:
        layout                  = QVBoxLayout()
        self.__products_widget  = ProductsWidget(self.__main_window, True, True, self.__main_window.device_setup["shownProducts"],
                                                 self.__main_window.products_details)
        self.__products_widget.SelectedProduct.connect(self.__on_product_selected)
        layout.addWidget(self.__products_widget)

        return layout
    

    def __on_product_selected(self, id) :
        self.__logger.debug (f"Selected product with id {id}. Do something!!!")


    def get_selected_products_tab(self):
        return self.__products_widget.get_selected_proucts_tab()
    
    def set_selected_products_tab(self, tab_idx):
        return self.__products_widget.set_selected_proucts_tab(tab_idx)