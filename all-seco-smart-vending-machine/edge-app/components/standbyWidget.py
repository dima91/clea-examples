
import os
from utils import commons
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


class StandbyWidget (QWidget) :

    ##########
    ## Members
    ##########
    __curr_image_idx    = 0
    __images            = []
    __image_label       = None
    __seco_logo_pixmap  = None
    __clea_logo_pixmap  = None
    __icon_size         = QSize(170, 170)


    def __init__(self, config, screen_sizes) -> None:
        super().__init__()

        # Loading signage images
        base_folder     = config['digital_signage']['base_folder']
        for path in os.listdir(base_folder):
            if os.path.isfile(os.path.join(base_folder, path)):
                full_path   = commons.get_abs_path (base_folder, path)
                print (f"Loading {full_path}")
                tmp_pixmap  = commons.resize_image(QPixmap(full_path), QSize(screen_sizes.width()*0.8, screen_sizes.height()*0.8))
                self.__images.append(tmp_pixmap)

        # TODO Loading footer images
        hbox    = QHBoxLayout()
        hbox.addWidget (self.__load_icon(config['digital_signage']['seco_logo_path']))
        hbox.addStretch(1)
        hbox.addWidget (self.__load_icon(config['digital_signage']['clea_logo_path']))
        footer  = QWidget()
        footer.setLayout(hbox)


        vbox                = QVBoxLayout()
        self.__image_label  = QLabel()
        self.__image_label.setPixmap(self.__images[0])
        vbox.addWidget(self.__image_label)
        vbox.addStretch(1)
        vbox.addWidget(footer)

        self.setLayout(vbox)


    def __load_icon(self, path) :
        tmp_pixmap  = commons.resize_image(QPixmap(path), self.__icon_size)
        tmp_label   = QLabel()
        tmp_label.setPixmap(tmp_pixmap)
        return tmp_label
        


    def start(self) :
        #TODO
        pass


    def stop(self) :
        #TODO
        pass