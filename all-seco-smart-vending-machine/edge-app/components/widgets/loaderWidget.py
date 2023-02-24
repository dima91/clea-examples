
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QMovie


class LoaderWidget (QWidget) :

    ##########
    ## Members
    ##########
    __movie = None
    ##########


    def __init__(self, config, scale_sizes) -> None:
        super().__init__()

        loader_path = config["loader"]["loader_path"]

        # Loading GIF
        self.__movie    = QMovie(loader_path)
        self.__movie.jumpToFrame (0)
        movie_w = self.__movie.currentImage().size().width()
        movie_h = self.__movie.currentImage().size().height()
        self.setGeometry(QRect(0, 0, movie_w, movie_h))

        # Assigning GIF to label
        label   = QLabel (self)
        label.setMovie(self.__movie)
        label.setScaledContents(True)

        # Placing label centered in parent class
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    
    def start (self) :
        self.__movie.start()

    def stop (self) :
        self.__movie.stop()

    def restart (self):
        self.__movie.stop()
        self.__movie.jumpToFrame(0)
        self.__movie.start()