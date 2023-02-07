
import os
from enum import Enum
from PySide6.QtCore import Qt


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


def create_logger (logging_ns, name):
    logger  = logging_ns.getLogger(name)
    return logger



def get_abs_path (base_folder, file_name) :
    return os.path.abspath(os.path.join(base_folder, file_name))


def resize_image (curr_pixmap, target_size) :
    return curr_pixmap.scaled(target_size, Qt.KeepAspectRatio)