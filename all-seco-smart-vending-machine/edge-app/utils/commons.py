
from enum import Enum
import os


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


def get_abs_path (base_folder, file_name) :
    return os.path.abspath(os.path.join(base_folder, file_name))