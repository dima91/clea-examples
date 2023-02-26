
import os, datetime, logging
import numpy as np
from enum import Enum

from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPixmap, QImage, QPainter, QPainterPath


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


'''
Session performed by the customer, starting from its detection by the camera and ending when it returns in the STANDBY status
It contains all the information taken in each step
'''
class CustomerSession():

    previous_status = None
    current_status  = None

    start_time                  = None
    frame                       = None
    face_detection_results      = None
    inference_results           = None
    current_product_tab_id      = None
    shown_advertisement_id      = None
    chosen_product_id           = None
    is_suggested_chosen_product = None

    def __init__(self) -> None:
        self.current_status         = Status.STANDBY
        self.current_product_tab_id = 0


class ProductsCardSize(Enum):
    SMALL   = 0
    LARGE   = 1


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


def create_logger (name):
    logger  = logging.getLogger(name)
    return logger


def get_abs_path (base_folder, file_name) :
    return os.path.abspath(os.path.join(base_folder, file_name))


def remove_shown_widget (widgets_stack) :
    shown_widget    = widgets_stack.currentWidget()
    if shown_widget:
        widgets_stack.removeWidget(shown_widget)


def remove_and_set_new_shown_widget (widgets_stack, new_widget):
    remove_shown_widget(widgets_stack)
    widgets_stack.setCurrentIndex(widgets_stack.addWidget(new_widget))


###################
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
    img_cropped     = img_pixmap.copy(QRect(a.x(), a.y(), b.x()-a.x(), b.y()-a.y()))
    frame_cropped   = cv_img[a.y():b.y(), a.x():b.x(), :]
    return (img_cropped, frame_cropped)


def midpoint(a, b):
    return [((a[0]+b[0])/2), ((a[1]+b[1])/2)]


def apply_border_radius(in_pix:QPixmap, radius, size) -> QPixmap:
    out_pix = QPixmap(size)
    out_pix.fill(Qt.transparent)

    path = QPainterPath()
    path.addRoundedRect(0, 0, in_pix.width(), in_pix.height(), radius, radius)
    
    painter = QPainter(out_pix)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, in_pix)

    return out_pix