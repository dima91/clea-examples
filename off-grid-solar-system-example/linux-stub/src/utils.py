
import enum, random


class DayPeriod(enum.Enum):
    NIGHT   = 0
    DAY     = 1


def get_random_value(base_value:float, error_percentage:float) -> float:
    error_value = base_value*error_percentage
    return base_value+random.uniform(-error_value, error_value)