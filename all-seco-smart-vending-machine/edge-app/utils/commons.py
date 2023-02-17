
import os, cv2, datetime
import numpy as np
from enum import Enum
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPixmap, QImage


class Status(Enum):
    INITIALIZING        = -1
    STANDBY             = 0
    RECOGNITION         = 1
    SUGGESTION          = 2
    SELECTION           = 3
    PAYMENT_REQUESTED   = 4
    PAYMENT_PROCESSING  = 5
    PAYMENT_ACCEPTED    = 6
    DISPENSING          = 7
    DISPENSED           = 8


def status_to_string (s) :
    result  = ""
    if s == Status.INITIALIZING:
        result  = "INITIALIZING"
    elif s == Status.STANDBY:
        result  = "STANDBY"
    elif s == Status.RECOGNITION:
        result  = "RECOGNITION"
    elif s == Status.SUGGESTION:
        result  = "SUGGESTION"
    elif s == Status.SELECTION:
        result  = "SELECTION"
    elif s == Status.PAYMENT_REQUESTED:
        result  = "PAYMENT_REQUESTED"
    elif s == Status.PAYMENT_PROCESSING:
        result  = "PAYMENT_PROCESSING"
    elif s == Status.PAYMENT_ACCEPTED:
        result  = "PAYMENT_ACCEPTED"
    elif s == Status.DISPENSING:
        result  = "DISPENSING"
    elif s == Status.DISPENSED:
        result  = "DISPENSED"
    else :
        result  = "<UNKNOWN STATE>"

    return result


emotions = ['Neutral', 'Happy', 'Sad', 'Surprise', 'Anger']


def ms_timestamp():
    return int(datetime.datetime.now().timestamp()*1000)


def create_logger (logging_ns, name):
    logger  = logging_ns.getLogger(name)
    return logger


def get_abs_path (base_folder, file_name) :
    return os.path.abspath(os.path.join(base_folder, file_name))


def remove_shown_widget (widgets_stack) :
    shown_widget    = widgets_stack.currentWidget()
    if shown_widget:
        widgets_stack.removeWidget(shown_widget)


## Images functions

        
def resize_image (curr_pixmap, target_size) :
    return curr_pixmap.scaled(target_size, Qt.KeepAspectRatio)


def cv_img_to_qt_pixmap(cv_img, target_size):
    """Convert from an opencv image to QPixmap"""
    h, w, ch        = cv_img.shape
    bytes_per_line  = ch * w
    q_img           = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
    raw_img         = resize_image(q_img, target_size)
    return QPixmap.fromImage(raw_img)


def get_cv_img_resolution(cv_img):
    return QSize (float(cv_img.shape[1]), float(cv_img.shape[0]))


def crop_image(cv_img, resolution, a, b) :
    # Cropping Pixmap && matrix
    img_pixmap      = cv_img_to_qt_pixmap(cv_img, resolution)
    img_cropped     = img_pixmap.copy(QRect(a.x, a.y, b.x-a.x, b.y-a.y))
    frame_cropped   = cv_img[a.y:b.y, a.x:b.x, :]
    return (img_cropped, frame_cropped)


def midpoint(a, b):
    # TODO Find better solution
    return [((a[0]+b[0])/2), ((a[1]+b[1])/2)]