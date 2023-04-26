
from typing import Tuple
import enum, random, math
from datetime import datetime


class DayPeriod(enum.Enum):
    NIGHT   = 0
    DAY     = 1


def get_random_value(base_value:float, error_percentage:float) -> float:
    error_value = base_value*error_percentage
    return base_value+random.uniform(-error_value, error_value)


# Return value unit: W/m²
#   "panel_size" is the ssolar panel dimension as a percentage of one m²
def solar_power_to_watts(panel_size:float, day_period:DayPeriod, current_irradiance:float,
                         cloud_cover_percentage:float, sunrise_sunset_times:Tuple[datetime, datetime]) -> float:
        if day_period == DayPeriod.NIGHT:
            print("It's night")
            return 0
        
        return panel_size*current_irradiance
        
        # It depends also on day hour respect to sunset and sunrise: sqrt(day_percentage)
        sunrise_t, sunset_t = sunrise_sunset_times
        now                 = datetime.now()

        sunrise_minutes     = (sunrise_t.hour*60)+sunrise_t.minute
        sunset_minutes      = (sunset_t.hour*60)+sunset_t.minute
        solar_minutes       = sunset_minutes-sunrise_minutes
        curr_minutes_norm   = (now.hour*60)+now.minute-sunrise_minutes
        day_percentage      = 1

        if curr_minutes_norm<(solar_minutes/2):
            day_percentage  = curr_minutes_norm/(solar_minutes/2)
        else:
            day_percentage  = 1-((curr_minutes_norm-(solar_minutes/2))/(solar_minutes/2))
        day_percentage  = math.sqrt(day_percentage)
        
        print(f'sunrise_minutes:{sunrise_minutes}, sunset_minutes:{sunset_minutes}, solar_minutes:{solar_minutes}, curr_minutes_norm:{curr_minutes_norm}, cloud_cover_percentage:{cloud_cover_percentage}, day_percentage:{day_percentage}')

        return (max_power-(max_power*cloud_cover_percentage))*day_percentage