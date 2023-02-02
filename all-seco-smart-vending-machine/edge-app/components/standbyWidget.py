
import os
from utils import commons
from PySide6.QtWidgets import QStackedWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


class StandbyWidget (QWidget) :

    def __init__(self, root_window, config) -> None:
        super(QWidget, self).__init__()

        # Loading images
        images_paths    = []
        base_folder     = config['digital_signage']['base_folder']
        for path in os.listdir(base_folder):
            if os.path.isfile(os.path.join(base_folder, path)):
                images_paths.append (commons.get_abs_path (base_folder, path))
        print (f'images_path {images_paths}')   # FIXME Debug print

        # TODO Loading footer images

