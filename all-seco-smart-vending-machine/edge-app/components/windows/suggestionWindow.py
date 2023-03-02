
from utils import commons
from utils.commons import Status
from components.widgets.videoWidget import VideoWidget
from components.widgets.suggestionWidget import SuggestionWidget
from components.widgets.footerWidget import FooterWidget
from components.widgets.productsWidget import ProductsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, QTimer, QSize

import logging


class SuggestionWindow (QWidget):

    __logger            = None
    __timer             = None
    __main_window       = None
    __products_widget   = None
    ##########
    EscapedCustomer = Signal()
    SelectedProduct = Signal(str, bool, float)     # product_id, is_suggested, promo_discount


    ##########


    def __init__(self, config, main_window, video_thread) -> None:
        super().__init__()

        self.__logger       = commons.create_logger(__name__)
        self.__main_window  = main_window
        # Adding a timeout to came back to standby
        timer_interval  = int(config["ai"]["escaped_customer_threshold_ms"])
        self.__timer    = QTimer()
        self.__timer.timeout.connect (self.__on_escaped_customer_timer_timeout)
        self.__timer.setSingleShot(True)
        self.__timer.setInterval(timer_interval)
        # Registering slot for session change
        main_window.SessionUpdate.connect(self.__on_session_change)

        hbox        = QHBoxLayout()
        hbox.addLayout(self.__build_lbox_layout(config, video_thread))
        hbox.addLayout(self.__build_rbox_layout())

        self.setLayout(hbox)


    def __on_session_change(self, current_session):
        if current_session.current_status == Status.SUGGESTION :
            self.__suggestion_widget.update_suggested_products(current_session)
            self.__timer.start()
        else :
            self.__timer.stop()


    def __on_escaped_customer_timer_timeout(self) -> None:
        self.EscapedCustomer.emit()


    def __build_lbox_layout(self, config, video_thread):
        layout  = QVBoxLayout()

        # Video widget
        vw_layout   = QHBoxLayout ()
        vw_layout.addStretch(1)
        vw_layout.addWidget(VideoWidget(self.__main_window, video_thread))
        vw_layout.addStretch(1)
        layout.addLayout(vw_layout)

        # Suggestion widget
        self.__suggestion_widget   = SuggestionWidget(self.__main_window, False)
        self.__suggestion_widget.SelectedProduct.connect(self.__on_suggested_product_select)
        layout.addWidget(self.__suggestion_widget)
        #layout.addStretch(1)
        layout.addWidget(FooterWidget(config, QSize(100, 100), None))

        return layout


    def __build_rbox_layout(self):
        layout                  = QVBoxLayout()
        self.__products_widget  = ProductsWidget(self.__main_window, True, True, self.__main_window.device_setup["device"]["shownProducts"],
                                                 self.__main_window.products_details)
        self.__products_widget.SelectedProduct.connect(self.__on_product_selected)
        layout.addWidget(self.__products_widget)

        return layout
    

    def __on_product_selected(self, id) :
        self.__logger.debug (f"Selected product with id {id}")
        self.SelectedProduct.emit (id, False, 0)


    def __on_suggested_product_select(self, id, promo_discount):
        self.__logger.debug (f"Selected SUGGESTED product with id {id}")
        self.SelectedProduct.emit (id, True, promo_discount)


    def get_selected_products_tab(self):
        return self.__products_widget.get_selected_proucts_tab()
    
    def set_selected_products_tab(self, tab_idx):
        return self.__products_widget.set_selected_proucts_tab(tab_idx)
    
    def update_suggested_products(self, session):
        self.__suggestion_widget.update_suggested_products(session)