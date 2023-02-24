
from utils import commons
from components.widgets.productsTable import ProductsTable

from PySide6.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QStackedWidget, QPushButton)
from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QColor


class ProductsWidget (QWidget):


    # FIXME Implement me!
    class __FakeButton(QLabel):
        def __init__(self):
            pass


    __logger            = None
    __main_window       = None
    __tables_stack      = None
    __selected_tab_idx  = None
    __sections          = None
    ##########
    SelectedProduct     = Signal(str)


    def __init__(self, main_window) -> None:
        QWidget.__init__(self)

        self.__logger           = commons.create_logger(__name__)
        self.__main_window      = main_window
        # Collecting sections
        self.__sections = []
        shown_prods     = main_window.device_setup["shownProducts"]
        prods_details   = main_window.products_details
        for i in shown_prods :
            s   = prods_details[i]['menuSection']
            if not s in self.__sections:
                self.__sections.append(s)

        root_layout = QVBoxLayout(self)
        
        # Adding the label
        label   = QLabel("Other drinks you might like...")
        label.setObjectName("ProductsLabel")
        root_layout.addWidget(label)

        # Creating "left" and "right" buttons
        left_button             = QPushButton("<")
        left_button.clicked.connect(self.__handle_l_button_pressed)
        right_button            = QPushButton(">")
        right_button.clicked.connect(self.__handle_r_button_pressed)

        switch_buttons_layout   = QHBoxLayout()
        switch_buttons_layout.addWidget(left_button)
        switch_buttons_layout.addStretch(1)
        switch_buttons_layout.addWidget(right_button)
        root_layout.addLayout(switch_buttons_layout)

        # Creating products tables
        self.__tables_stack = QStackedWidget()
        for s in self.__sections:
            prod_table  = ProductsTable(self.__main_window, s)
            prod_table.SelectedProduct.connect(self.__on_selected_product)
            self.__tables_stack.addWidget(prod_table)
        
        self.__selected_tab_idx = 1
        self.__tables_stack.setCurrentIndex(self.__selected_tab_idx)
        root_layout.addWidget(self.__tables_stack)

        self.setLayout(root_layout)


    def __handle_l_button_pressed(self, evt) :
        print ("L buton pressed!")
        self.set_selected_proucts_tab((self.__selected_tab_idx-1)%len(self.__sections))

    
    def __handle_r_button_pressed(self, evt) :
        print ("R button pressed!")
        self.set_selected_proucts_tab((self.__selected_tab_idx+1)%len(self.__sections))


    def __on_selected_product(self, id) :
        self.SelectedProduct.emit(id)


    def get_selected_proucts_tab(self):
        return self.__selected_tab_idx
    

    def set_selected_proucts_tab(self, idx):
        if idx>=0 and idx<len(self.__sections):
            self.__selected_tab_idx = idx
            self.__tables_stack.setCurrentIndex(self.__selected_tab_idx)