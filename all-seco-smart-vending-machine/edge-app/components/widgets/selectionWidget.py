
from utils import commons
from utils.commons import Status
from utils.commons import CustomerSession
from components.widgets.sugarWidget import SugarWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap


class SelectionWidget(QWidget):

    __main_window       = None
    __logger            = None
    __min_image_width   = None
    __min_image_height  = None
    ##########
    SelectionConfirmed  = Signal(bool)


    def __init__(self, main_window, session) -> None:
        super().__init__()

        self.__main_window      = main_window
        self.__logger           = commons.create_logger(__name__)
        self.__min_image_width  = int(main_window.get_config()["selection"]["min_image_width"])
        self.__min_image_height = int(main_window.get_config()["selection"]["min_image_height"])
        self.__init_ui(session)


    def __init_ui(self, session:CustomerSession):
        if session.current_status == Status.SELECTION:
            product = self.__main_window.products_details[session.chosen_product_id]
            self.__logger.debug(f"Updating with product:\n{product}")

            text_layout = QHBoxLayout()
            text_label  = QLabel("Your selection:")
            text_label.setObjectName("SelectionLabel")
            text_layout.addWidget(text_label)
            #text_layout.addStretch(1)

            image_label = QLabel()
            pixmap      = self.__main_window.images_repository.get_pixmap(product["imagePath"])
            image_label.setPixmap(commons.resize_image(pixmap, QSize(self.__min_image_width, self.__min_image_height)))

            back_button     = QPushButton("BACK")
            back_button.setObjectName("ConfirmationButton")
            back_button.clicked.connect(lambda evt: self.SelectionConfirmed.emit(False))
            confirm_button  = QPushButton("CONFIRM")
            confirm_button.setObjectName("ConfirmationButton")
            confirm_button.clicked.connect(lambda evt: self.SelectionConfirmed.emit(True))
            buttons_layout  = QHBoxLayout()
            buttons_layout.addStretch(4)
            buttons_layout.addWidget(back_button)
            buttons_layout.addStretch(2)
            buttons_layout.addWidget(confirm_button)
            buttons_layout.addStretch(4)
            
            buttons_widget   = QWidget()
            buttons_widget.setObjectName("ButtonsWidget")
            buttons_widget.setLayout(buttons_layout)

            root_layout = QVBoxLayout()

            root_layout.addLayout(text_layout)
            root_layout.addStretch(1)
            
            root_layout.addLayout(commons.h_center_widget(image_label))

            product_name    = QLabel(product["name"])
            product_name.setObjectName("Selection_ProductName")
            root_layout.addStretch(2)
            root_layout.addLayout(commons.h_center_widget(product_name))

            real_price  = product["currentPrice"]
            if session.promo_discount!=0:
                real_price      =real_price - (real_price*session.promo_discount/100)
            product_price   = QLabel(f'{str(real_price)} €')
            product_price.setObjectName("Selection_ProductCost")
            root_layout.addStretch(1)
            root_layout.addLayout(commons.h_center_widget(product_price))

            if product["needsSugar"]:
                root_layout.addStretch(1)
                root_layout.addLayout(commons.h_center_widget(SugarWidget()))
            root_layout.addStretch(4)
            root_layout.addWidget(buttons_widget)
            root_layout.addStretch(1)

            self.setLayout(root_layout)