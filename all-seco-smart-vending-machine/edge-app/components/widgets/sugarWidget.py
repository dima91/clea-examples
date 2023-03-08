
from utils import commons

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame


class SugarWidget(QWidget):

    __SUGAR_INDICATORS_COUNT    = 5

    __sugar_level               = 3
    __sugar_indicators_list     = []
    ##########

    
    def __init__(self) -> None:
        super().__init__()

        minus_button    = QPushButton("-")
        minus_button.setObjectName("MinusPlusButton")
        minus_button.clicked.connect(self.__decrease_sugar_level)
        plus_button     = QPushButton("+")
        plus_button.setObjectName("MinusPlusButton")
        plus_button.clicked.connect(self.__increase_sugar_level)

        suugar_label    = QLabel("Sugar")
        suugar_label.setObjectName("SugarLabel")

        self.__build_sugar_indicators()

        root_layout     = QHBoxLayout()
        root_layout.addStretch(4)
        root_layout.addWidget(suugar_label)
        root_layout.addStretch(1)
        root_layout.addWidget(minus_button)
        for i in range(self.__SUGAR_INDICATORS_COUNT):
            root_layout.addWidget(self.__sugar_indicators_list[i])
        root_layout.addWidget(plus_button)
        root_layout.addStretch(4)

        self.setLayout(root_layout)
        self.__on_sugar_level_changed()


    def __build_sugar_indicators(self) -> QLabel:
        for i in range(self.__SUGAR_INDICATORS_COUNT):
            indicator   = QLabel()
            indicator.setObjectName("SugarIndicator")
            self.__sugar_indicators_list.append(indicator)
        
        return indicator
    
    def __increase_sugar_level(self, e):
        if self.__sugar_level<self.__SUGAR_INDICATORS_COUNT:
            self.__sugar_level += 1
            self.__on_sugar_level_changed()

    def __decrease_sugar_level(self, e):
        if self.__sugar_level>0:
            self.__sugar_level -= 1
            self.__on_sugar_level_changed()
    

    def __on_sugar_level_changed(self):
        for i in range(self.__SUGAR_INDICATORS_COUNT):
            if i<self.__sugar_level:
                self.__sugar_indicators_list[i].setStyleSheet("QLabel{background-color:blue}")
            else:
                self.__sugar_indicators_list[i].setStyleSheet("QLabel{background-color:grey}")
