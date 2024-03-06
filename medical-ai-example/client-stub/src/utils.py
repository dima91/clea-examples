from datetime import datetime
from enum import Enum

class EventType(Enum):
    Normal  = "NORMAL"
    Warning = "WARNING"
    Alert   = "ALERT"


__DATE_TIME_FORMAT  = "%Y/%m/%d %H:%M:%S"
__TIME_FORMAT       = "%H:%M:%S"

def parse_string_datetime(dt_str:str) -> datetime:
    return datetime.strptime(dt_str, __DATE_TIME_FORMAT)

def parse_string_time(t_str:str) -> datetime:
    return datetime.strptime(t_str, __TIME_FORMAT)


def format_datetime(dt:datetime) -> str:
    return datetime.strftime(dt, __DATE_TIME_FORMAT)

def format_time(dt:datetime) -> str:
    return datetime.strftime(dt, __TIME_FORMAT)