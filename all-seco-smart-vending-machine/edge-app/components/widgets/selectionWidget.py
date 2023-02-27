
from utils import commons
from utils.commons import Status
from components.widgets.sugarWidget import SugarWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap


class SelectionWidget(QWidget):

    __main_window       = None
    __logger            = None
    ##########
    SelectionConfirmed  = Signal(bool)


    def __init__(self, main_window, session) -> None:
        super().__init__()

        self.__main_window  = main_window
        self.__logger       = commons.create_logger(__name__)
        self.__init_ui(session)


    def __init_ui(self, session):
        if session.current_status == Status.SELECTION:
            product = self.__main_window.products_details[session.chosen_product_id]
            self.__logger.debug(f"Updating with product:\n{product}")
            
            root_layout = QVBoxLayout()
            self.setLayout(root_layout)

            text_layout = QHBoxLayout()
            text_label  = QLabel("Your selection:")
            text_layout.addWidget(text_label)
            text_layout.addStretch(1)

            image_label = QLabel()
            pixmap      = QPixmap()
            pixmap.load(product["imagePath"])
            image_label.setPixmap(commons.resize_image(pixmap, QSize(500, 500)))

            back_button     = QPushButton("Back")
            back_button.clicked.connect(lambda evt: self.SelectionConfirmed.emit(False))
            confirm_button  = QPushButton("Confirm")
            confirm_button.clicked.connect(lambda evt: self.SelectionConfirmed.emit(True))
            buttons_layout  = QHBoxLayout()
            buttons_layout.addStretch(2)
            buttons_layout.addWidget(back_button)
            buttons_layout.addStretch(1)
            buttons_layout.addWidget(confirm_button)
            buttons_layout.addStretch(2)

            root_layout.addLayout(text_layout)
            root_layout.addLayout(commons.h_center_widget(image_label))
            root_layout.addLayout(commons.h_center_widget(QLabel(product["name"])))
            root_layout.addLayout(commons.h_center_widget(QLabel(str(product["currentPrice"]))))
            if product["needsSugar"]:
                root_layout.addLayout(commons.h_center_widget(SugarWidget()))
            root_layout.addStretch(1)
            root_layout.addLayout(buttons_layout)

            self.setLayout(root_layout)