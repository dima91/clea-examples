
from utils import commons
from components.widgets.productsTable import ProductsTable

from PySide6.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QStackedWidget, QPushButton)
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QColor


class ProductsWidget (QWidget):


    # FIXME Implement me! -> Class for left and right buttons (?)
    class __FakeButton(QLabel):
        def __init__(self):
            pass


    __logger            = None
    __main_window       = None
    __tables_stack      = None
    __selected_tab_idx  = None
    __sections          = None
    __current_section   = None
    __show_sections     = None
    __config            = None
    ##########
    SelectedProduct     = Signal(str)


    def __init__(self, main_window, show_title, separate_in_sections, shown_products, products_details,
                 promo_descriptor=None, promo_poduct_id=None) -> None:
        QWidget.__init__(self)

        self.__logger           = commons.create_logger(__name__)
        self.__main_window      = main_window
        self.__config           = self.__main_window.get_config()
        self.__show_sections    = separate_in_sections
        self.__main_window.SessionUpdate.connect(self.__on_session_change)
        # Collecting sections
        self.__sections = []
        if separate_in_sections :
            for i in shown_products:
                s   = products_details[i]['menuSection']
                if not s in self.__sections:
                    self.__sections.append(s)

        root_layout = QVBoxLayout(self)
        
        # Adding the label
        if show_title:
            label   = QLabel("Other drinks you might like...")
            label.setObjectName("ProductsLabel")
            root_layout.addWidget(label)

        if separate_in_sections:
            # Creating "left" and "right" buttons and section label
            left_button             = QPushButton("<")
            left_button.setObjectName("SectionSelector")
            left_button.clicked.connect(self.__handle_l_button_pressed)
            
            right_button            = QPushButton(">")
            right_button.setObjectName("SectionSelector")
            right_button.clicked.connect(self.__handle_r_button_pressed)
            
            self.__current_section  = QLabel("")
            self.__current_section.setObjectName("ProductsSection")

            switch_buttons_layout   = QHBoxLayout()
            switch_buttons_layout.addWidget(left_button)
            switch_buttons_layout.addStretch(1)
            switch_buttons_layout.addWidget(self.__current_section)
            switch_buttons_layout.addStretch(1)
            switch_buttons_layout.addWidget(right_button)
            root_layout.addLayout(switch_buttons_layout)

        # Creating products tables
        self.__tables_stack = QStackedWidget()
        if separate_in_sections:
            for s in self.__sections:
                # Filtering products by target section
                prods_id    = filter (lambda e: products_details[e]["menuSection"] == s, products_details)
                # Building and configuring ProductsTable
                prod_table  = ProductsTable(self.__main_window, prods_id, products_details, commons.ProductsCardSize.LARGE,
                                            promo_descriptor, promo_poduct_id)
                prod_table.SelectedProduct.connect(self.__on_selected_product)
                self.__tables_stack.addWidget(prod_table)
        else :
            prod_table  = ProductsTable(self.__main_window, shown_products, products_details, commons.ProductsCardSize.SMALL,
                                        promo_descriptor, promo_poduct_id)
            prod_table.SelectedProduct.connect(self.__on_selected_product)
            self.__tables_stack.addWidget(prod_table)
        
        self.set_selected_proucts_tab(0)
        root_layout.addWidget(self.__tables_stack)

        self.setLayout(root_layout)


    def __on_session_change(self, session):
        self.set_selected_proucts_tab(session.current_product_tab_id)


    def __handle_l_button_pressed(self, evt) :
        self.set_selected_proucts_tab((self.__selected_tab_idx-1)%len(self.__sections))

    
    def __handle_r_button_pressed(self, evt) :
        self.set_selected_proucts_tab((self.__selected_tab_idx+1)%len(self.__sections))


    def __on_selected_product(self, id) :
        self.SelectedProduct.emit(id)


    def get_selected_proucts_tab(self):
        return self.__selected_tab_idx
    

    def set_selected_proucts_tab(self, idx):
        if (idx>=0 and idx<len(self.__sections)) or self.__show_sections==False:
            self.__selected_tab_idx = idx
            self.__tables_stack.setCurrentIndex(self.__selected_tab_idx)
            if self.__show_sections:
                self.__current_section.setText(self.__sections[self.__selected_tab_idx])