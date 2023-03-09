
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from utils import commons


class FooterWidget (QWidget) :

    ##########


    def __init__(self, config, icons_size, middle_text) -> None:
        super().__init__()

        text_label  = QLabel(middle_text)
        text_label.setObjectName("FooterText")

        hbox    = QHBoxLayout()
        hbox.addWidget (self.__load_icon(config['footer']['seco_logo_path'], icons_size))
        hbox.addStretch(1)
        if middle_text :
            hbox.addWidget (text_label)
        hbox.addStretch(1)
        hbox.addWidget (self.__load_icon(config['footer']['clea_logo_path'], icons_size))
        self.setLayout(hbox)


    def __load_icon(self, path, size) :
        tmp_pixmap  = commons.resize_image(QPixmap(path), size)
        tmp_label   = QLabel()
        tmp_label.setPixmap(tmp_pixmap)
        #print (f"----> {path} : {tmp_label.geometry()}")
        return tmp_label