
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QWidget, QLabel, QFrame
from PySide6.QtGui import QMovie


class LoaderWidget (QWidget) :

    def __init__(self, root_window, config) -> None:
        super().__init__()

        print (f'Loading loader -> {config["loader"]["loader_path"]}')

        self.label = QLabel(self)
        self.movie = QMovie(config["loader"]["loader_path"])
        self.label.setMovie(self.movie)
        #print (Qt.AlignmentFlag)
        #self.label.setAlignment (Qt.AlignmentFlag.AlignCenter)
        
        self.movie.jumpToFrame (0)
        movie_w     = self.movie.currentImage().size().width()
        movie_h     = self.movie.currentImage().size().height()
        print (f"{movie_w} - {movie_h}")
        
        self.setGeometry(QRect(0, 0, movie_w, movie_h))
        
        self.movie.start()