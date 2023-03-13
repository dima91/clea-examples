
from utils import commons
from components.widgets.CardWidget import CardWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QProgressBar
from PySide6.QtCore import Signal, QTimer, QPoint, Qt
from PySide6.QtGui import QColor, QPalette, QPixmap

from enum import Enum


class DispensingStatus(Enum):
    STOPPED     = 0
    STARTED     = 1
    FINISHED    = 2


class DispensingWidget(QWidget):

    __DISPENSING_MAX_QUANTITY       = 100
    __DISPENSING_STEP_QUANTITY      = 5
    __DISPENSING_STEP_DRATUION_MS   = 100
    __STOPPED_STATUS_TIMER_DELAY    = 8000
    __CARD_WIDTH                    = None
    __CARD_HEIGHT                   = None

    __stacket_widget        = None
    __d_shadow              = None
    __p_shadow              = None

    __progress_bar_label    = None
    __dispensing_timer      = None
    __dispensing_status     = None
    __dispensed_quantity    = None
    __stopped_status_timer  = None
    __dispensed_pixmap      = None
    ##########
    DispensingUpdate    = Signal(DispensingStatus)

    
    def __init__(self, cards_size, dispensed_img_path) -> None:
        super().__init__()

        self.__stacket_widget   = QStackedWidget()
        self.__CARD_WIDTH       = cards_size.width()
        self.__CARD_HEIGHT      = cards_size.height()
        root_layout             = QVBoxLayout()
        root_layout.addLayout(commons.h_center_widget(self.__stacket_widget))

        self.setLayout(root_layout)

        self.__dispensing_status    = DispensingStatus.STOPPED
        self.__dispensing_timer     = QTimer(self)
        self.__dispensing_timer.setInterval(self.__DISPENSING_STEP_DRATUION_MS)
        self.__dispensing_timer.timeout.connect(self.__dispensing_timer_cb)
        self.__dispensed_pixmap     = QPixmap()
        self.__dispensed_pixmap.load(dispensed_img_path)


    def __build_dispensing_card(self):
        self.__progress_bar = QProgressBar()
        inner_layout        = QVBoxLayout()
        self.__progress_bar.setObjectName("DispensingProgressBar")

        p = QPalette()
        if self.__dispensed_quantity==self.__DISPENSING_MAX_QUANTITY:
            p.setColor(QPalette.Highlight, Qt.green)
        else:
            p.setColor(QPalette.Highlight, Qt.blue)
        self.__progress_bar.setPalette(p)
        self.__progress_bar.setTextVisible(False)
        self.__progress_bar.setRange(0, self.__DISPENSING_MAX_QUANTITY)
        self.__progress_bar.setValue(self.__percentage(self.__dispensed_quantity, self.__DISPENSING_MAX_QUANTITY))
        
        dispensing_description  = QLabel("Dispensed" if self.__dispensed_quantity==self.__DISPENSING_MAX_QUANTITY else "Dispensing")
        dispensing_description.setObjectName("DispensingDescription")
        dispensing_status_str   = QLabel("Finish" if self.__dispensed_quantity==self.__DISPENSING_MAX_QUANTITY else "")
        dispensing_status_str.setObjectName("DispensingStatusStr")
        inner_layout.addWidget(dispensing_description)
        inner_layout.addWidget(self.__progress_bar)
        inner_layout.addWidget(dispensing_status_str)

        card    = CardWidget (inner_layout, QColor(190,190,190), 50, QPoint(5, 5), "dispensing_product_card")
        card.setObjectName("DispensingCard")
        card.setFixedSize(self.__CARD_WIDTH, self.__CARD_HEIGHT)

        return card
    
    
    def __build_product_ready_card(self):
        inner_layout    = QHBoxLayout()
        inner_layout.addStretch(1)
        pixmap_label    = QLabel()
        pixmap_label.setPixmap(self.__dispensed_pixmap)
        inner_layout.addWidget(pixmap_label)
        inner_layout.addStretch(4)
        ready_label     = QLabel("Your drink\nis\nREADY!")
        ready_label.setObjectName("ProductReadyLabel")
        inner_layout.addWidget(ready_label)
        inner_layout.addStretch(1)

        card    = CardWidget(inner_layout, QColor(190,190,190), 50, QPoint(5, 5), "product_ready_card")
        card.setObjectName("DispensingCard")
        card.setFixedSize(self.__CARD_WIDTH, self.__CARD_HEIGHT)
        
        return card


    def __dispensing_timer_cb(self):
        self.__dispensed_quantity += self.__DISPENSING_STEP_QUANTITY
        self.__progress_bar.setValue(self.__percentage(self.__dispensed_quantity, self.__DISPENSING_MAX_QUANTITY))
        
        if self.__dispensed_quantity == self.__DISPENSING_MAX_QUANTITY:
            self.__dispensing_timer.stop()
            self.__dispensing_status    = DispensingStatus.FINISHED
            root_widget                 = QWidget()
            root_layout                 = QVBoxLayout()
            root_layout.addStretch(1)
            root_layout.addWidget(self.__build_dispensing_card())
            root_layout.addStretch(1)
            root_layout.addWidget(self.__build_product_ready_card())
            root_layout.addStretch(4)
            root_widget.setLayout(root_layout)
            commons.remove_and_set_new_shown_widget(self.__stacket_widget, root_widget)

            self.DispensingUpdate.emit(self.__dispensing_status)

            # Starting timer to send STOPPED dispensing status
            self.__stopped_status_timer     = QTimer(self)
            self.__stopped_status_timer.setSingleShot(True)
            self.__stopped_status_timer.setInterval(self.__STOPPED_STATUS_TIMER_DELAY)
            self.__stopped_status_timer.timeout.connect(lambda : self.__update_status_and_emit_event(DispensingStatus.STOPPED))
            self.__stopped_status_timer.start()


    def __percentage(self, curr, max):
        return max/100*curr
    

    def __update_status_and_emit_event(self, target_status):
        self.__dispensing_status    = target_status
        self.DispensingUpdate.emit(self.__dispensing_status)


    def start_dispensing(self) -> None:
        if self.__dispensing_status != DispensingStatus.STOPPED:
            self.__logger.critical(f"Required to start dispensing but current status({self.__dispensing_status}) differs from that required ({DispensingStatus.STOPPED})")
        else :
            self.__dispensed_quantity   = 0
            self.__dispensing_status    = DispensingStatus.STARTED
            commons.remove_and_set_new_shown_widget(self.__stacket_widget, self.__build_dispensing_card())
            self.__dispensing_timer.start()
            self.DispensingUpdate.emit(self.__dispensing_status)