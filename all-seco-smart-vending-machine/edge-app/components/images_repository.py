
from utils import commons

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

import os, validators, requests


class ImageDescriptor():

    path    = None
    pixmap   = None
    ##########


    def __init__(self, path:str, pixmap:QPixmap) -> None:
        self.path   = path
        self.pixmap = pixmap


class ImagesRepository(QWidget):

    __images_descriptors    = {}
    ##########


    def __init__(self) -> None:
        super().__init__()


    def __retrieve_image(self, path) -> QPixmap:
        pixmap  = QPixmap()
        if validators.url(path) :
            pixmap.loadFromData(requests.get(path).content)
        else :
            pixmap.load(path)
        return pixmap


    def get_pixmap(self, path) -> QPixmap :
        
        # Checking if image_path is an URL or a file
        if validators.url(path) and os.path.isfile(path) :
            raise Exception(f"{path} is either a file and a URL")
        if not validators.url(path) and not os.path.isfile(path) :
            raise Exception(f"{path} is neither a file neither a URL")
        
        # Checking if 'path' already exists
        result  = self.__images_descriptors.get(path)
        if result==None:
            pixmap                          = self.__retrieve_image(path)
            result                          = ImageDescriptor(path, pixmap)
            self.__images_descriptors[path] = result
        else:
            #print(f"Image {path} already exists!\n\n")
            pass

        return result.pixmap.copy()