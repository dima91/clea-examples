
import os, datetime, logging, random, string, json
import numpy as np
from enum import Enum

from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage, QPainter, QPainterPath


class Status(Enum):
    INITIALIZING        = -1
    STANDBY             = 0
    RECOGNITION         = 1
    SUGGESTION          = 2
    SELECTION           = 3
    PAYMENT             = 4
    DISPENSING          = 5
    ERROR               = 6


'''
Session performed by the customer, starting from its detection by the camera and ending when it returns in the STANDBY status
It contains all the information taken in each step
'''
class CustomerSession():

    previous_status = None
    current_status  = None

    start_time                  = None
    end_time                    = None
    frame                       = None
    face_detection_results      = None
    inference_results           = None
    current_product_tab_id      = None
    shown_advertisement_id      = None
    chosen_product_id           = None
    promo_id                    = None
    promo_discount              = None
    transaction_id              = None
    is_chosen_product_suggested = None
    connected_dispenser_id      = None
    error_string                = None

    def __init__(self) -> None:
        self.current_status         = Status.STANDBY
        self.current_product_tab_id = 0

    def set_status(self, new_status:Status) -> None:
        self.current_status = new_status

    def start_session(self) -> None:
        start_time  = ms_timestamp()

    def close_session(self) -> int:
        self.end_time   = ms_timestamp()
        return self.end_time-self.start_time
    
    def new_detection(self, frame:object, detection_results:dict, inference_results:dict) -> None:
        self.frame                  = frame
        self.face_detection_results = detection_results
        self.inference_results      = inference_results

    def update_shown_advertisement(self, advertisement_id:str) -> None:
        self.shown_advertisement_id = advertisement_id

    def update_chosen_product(self, chosen_product_id:str, is_suggested:bool, promo_id:str, promo_discount:float, connected_dispenser_id:int) -> None:
        self.chosen_product_id              = chosen_product_id
        self.is_chosen_product_suggested    = is_suggested
        self.promo_discount                 = promo_discount
        self.promo_id                       = promo_id
        self.connected_dispenser_id         = connected_dispenser_id

    def update_transaction_id(self, transaction_id:str) -> None:
        self.transaction_id = transaction_id

    def set_error_string(self, err_str) -> None:
        self.error_string   = err_str

    def to_dict(self) -> dict:
        return {"previous_status":self.previous_status, "current_status":self.current_status, "start_time":self.start_time,
                "end_time":self.end_time, "frame":self.frame, "face_detection_results":self.face_detection_results,
                "inference_results":self.inference_results, "current_product_tab_id":self.current_product_tab_id,
                "shown_advertisement_id":self.shown_advertisement_id, "chosen_product_id":self.chosen_product_id,
                "promo_id":self.promo_id, "promo_discount":self.promo_discount, "transaction_id":self.transaction_id,
                "is_chosen_product_suggested":self.is_chosen_product_suggested}


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
    elif s == Status.PAYMENT:
        result  = "PAYMENT"
    elif s == Status.DISPENSING:
        result  = "DISPENSING"
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


def dict_to_pretty_print(d) -> str:
    return json.dumps(d, indent=3)


def remove_shown_widget (widgets_stack) :
    shown_widget    = widgets_stack.currentWidget()
    if shown_widget:
        widgets_stack.removeWidget(shown_widget)


def remove_and_set_new_shown_widget (widgets_stack, new_widget):
    remove_shown_widget(widgets_stack)
    widgets_stack.setCurrentIndex(widgets_stack.addWidget(new_widget))


def generate_random_id(length):
    source  = string.ascii_letters+string.digits
    result  = ''.join(random.choice(source) for i in range(length))
    return result


###################
## Images functions

        
def resize_image (curr_pixmap, target_size) -> QPixmap:
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


def apply_border_radius(in_pix:QPixmap, radius:int, size:QSize) -> QPixmap:
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


###################
## Layout functions

def h_center_widget(w) -> QHBoxLayout:
    h_layout    = QHBoxLayout()
    h_layout.addStretch(1)
    h_layout.addWidget(w)
    h_layout.addStretch(1)
    return h_layout

def v_center_widget(w) -> QVBoxLayout:
    v_layout    = QVBoxLayout()
    v_layout.addStretch(1)
    v_layout.addWidget(w)
    v_layout.addStretch(1)
    return v_layout

def hv_center_widget(w) -> QVBoxLayout:
    h_layout    = h_center_widget(w)
    v_layout    = QVBoxLayout()
    v_layout.addStretch(1)
    v_layout.addLayout(h_layout)
    v_layout.addStretch(1)