
from utils import commons

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class SugarWidget(QWidget):

    ##########

    
    def __init__(self) -> None:
        super().__init__()

        root_layout = QHBoxLayout()
        root_layout.addStretch(1)
        root_layout.addWidget(QLabel("Sugar"))
        root_layout.addWidget(QPushButton("-"))
        #TODO Add QRects to display currentsugar level
        root_layout.addWidget(QPushButton("+"))
        root_layout.addStretch(1)

        self.setLayout(root_layout)