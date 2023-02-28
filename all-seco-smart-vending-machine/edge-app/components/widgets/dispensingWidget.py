
from utils import commons
from components.widgets.CardWidget import CardWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QProgressBar
from PySide6.QtCore import Signal, QTimer, QPoint, Qt
from PySide6.QtGui import QColor, QPalette

from enum import Enum


class DispensingStatus(Enum):
    STOPPED     = 0
    STARTED     = 1
    FINISHED    = 2


class DispensingWidget(QWidget):

    __DISPENSING_MAX_QUANTITY       = 100
    __DISPENSING_STEP_QUANTITY      = 5
    __DISPENSING_STEP_DRATUION_MS   = 100
    __STOPPED_STATUS_TIMER_DELAY    = 3000

    __stacket_widget        = None
    __d_shadow              = None
    __p_shadow              = None

    __progress_bar_label    = None
    __dispensing_timer      = None
    __dispensing_status     = None
    __dispensed_quantity    = None
    __stopped_status_timer  = None
    ##########
    DispensingUpdate    = Signal(DispensingStatus)

    
    def __init__(self) -> None:
        super().__init__()

        self.__stacket_widget   = QStackedWidget()
        root_layout             = QVBoxLayout()
        root_layout.addLayout(commons.h_center_widget(self.__stacket_widget))

        self.setLayout(root_layout)

        self.__dispensing_status    = DispensingStatus.STOPPED
        self.__dispensing_timer     = QTimer(self)
        self.__dispensing_timer.setInterval(self.__DISPENSING_STEP_DRATUION_MS)
        self.__dispensing_timer.timeout.connect(self.__dispensing_timer_cb)


    def __build_dispensing_card(self):
        self.__progress_bar = QProgressBar()
        inner_layout        = QVBoxLayout()

        p = QPalette()
        p.setColor(QPalette.Highlight, Qt.green)
        self.__progress_bar.setPalette(p)
        self.__progress_bar.setTextVisible(False)
        self.__progress_bar.setRange(0, self.__DISPENSING_MAX_QUANTITY)
        self.__progress_bar.setValue(self.__percentage(self.__dispensed_quantity, self.__DISPENSING_MAX_QUANTITY))
        
        inner_layout.addWidget(QLabel("Dispensed" if self.__dispensed_quantity==self.__DISPENSING_MAX_QUANTITY else "Dispensing"))
        inner_layout.addWidget(self.__progress_bar)
        inner_layout.addWidget(QLabel("Fisnish" if self.__dispensed_quantity==self.__DISPENSING_MAX_QUANTITY else "I'm heating the milk..."))

        return CardWidget(inner_layout, QColor(190,190,190), 25, QPoint(10, 10), "dispensing_product_card")
    
    
    def __build_product_ready_card(self):
        inner_layout    = QHBoxLayout()
        inner_layout.addStretch(1)
        inner_layout.addWidget(QLabel("image"))    # TODO Insert image
        inner_layout.addStretch(1)
        inner_layout.addWidget(QLabel("Your drink\nis\nREADY!"))
        inner_layout.addStretch(1)
        
        return CardWidget(inner_layout, QColor(190,190,190), 25, QPoint(10,10), "product_ready_card")


    def __dispensing_timer_cb(self):
        self.__dispensed_quantity += self.__DISPENSING_STEP_QUANTITY
        self.__progress_bar.setValue(self.__percentage(self.__dispensed_quantity, self.__DISPENSING_MAX_QUANTITY))
        
        if self.__dispensed_quantity == self.__DISPENSING_MAX_QUANTITY:
            self.__dispensing_timer.stop()
            self.__dispensing_status    = DispensingStatus.FINISHED
            root_widget                 = QWidget()
            root_layout                 = QVBoxLayout()
            root_layout.addWidget(self.__build_dispensing_card())
            root_layout.addWidget(self.__build_product_ready_card())
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