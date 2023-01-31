
from PyQt6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


class StandbyWindow (QWidget) :

    def __init__(self, parent, config) -> None:
        super(QWidget, parent).__init__()