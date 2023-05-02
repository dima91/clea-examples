
import random


def generate_mac_address() -> str:
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),\
                                              random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def generate_float_with_error(base_value:float, error_percentage:float) -> float:
    error_value = base_value*error_percentage
    return base_value+random.uniform(-error_value, error_value)
