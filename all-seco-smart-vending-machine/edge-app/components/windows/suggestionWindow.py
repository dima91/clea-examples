
from utils import commons
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SuggestionWindow (QWidget):

    ## Members
    ##########


    def __init__(self, config, main_window) -> None:
        super().__init__()

        # FIXME TEST
        vbox    = QVBoxLayout()
        vbox.addWidget (QLabel("suggestionWindow"))
        self.setLayout(vbox)

        # TODO Adding a timeout to came back to standby -> EscapedCustomer