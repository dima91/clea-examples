
import math, random
from datetime import timedelta, datetime


# Return a value tending to 0 if curr_t is near max_t
def compute_min_probability_if_among(min_t, max_t, max_p, curr_t) :
    result  = 2
    if min_t <= curr_t <= max_t:
        time_range      = (max_t-min_t)
        time_delta      = max_t-curr_t
        time_percentage = time_delta.total_seconds()/time_range.total_seconds()
        # TODO Generate a min probability value with more accuracy
        result  = math.sqrt(time_percentage)
    return result


def compute_int_percentage(base_value:int, factor_range:list) -> int:
    curr_factor = random.uniform(factor_range[0], factor_range[1])
    curr_value  = int(round(base_value*curr_factor,0))
    return curr_value


ENTRANCE_PARAMS         = {
    "GET_START_TIME"        : lambda d,start_time_entrance_params : d.replace(hour=start_time_entrance_params["HOUR"],
                                                                              minute=start_time_entrance_params["MINUTE"],
                                                                              second=0, microsecond=0),
    "GET_END_TIME"          : lambda d,end_time_entrance_params : d.replace(hour=end_time_entrance_params["HOUR"],
                                                                            minute=end_time_entrance_params["MINUTE"],
                                                                            second=0, microsecond=0),
    "GET_MIN_PROBABILITY"   : lambda n,params,max_p : compute_min_probability_if_among(ENTRANCE_PARAMS["GET_START_TIME"](n,params["START_TIME"]),
                                                                                       ENTRANCE_PARAMS["GET_END_TIME"](n,params["END_TIME"]),
                                                                                       max_p, n)
}
EXIT_PARAMS             = {
    "GET_START_TIME"        : lambda d,start_time_exit_params : d.replace(hour=start_time_exit_params["HOUR"],
                                                                          minute=start_time_exit_params["MINUTE"],
                                                                          second=0, microsecond=0),
    "GET_END_TIME"          : lambda d,end_time_exit_params : d.replace(hour=end_time_exit_params["HOUR"],
                                                                        minute=end_time_exit_params["MINUTE"],
                                                                        second=0, microsecond=0),
    "GET_MIN_PROBABILITY"   : lambda n,params,max_p, : compute_min_probability_if_among(EXIT_PARAMS["GET_START_TIME"](n,params["START_TIME"]),
                                                                                        EXIT_PARAMS["GET_END_TIME"](n,params["END_TIME"]),
                                                                                        max_p, n)
}