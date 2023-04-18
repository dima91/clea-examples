
import math
from datetime import timedelta, datetime


# Return a value tending to 0 if curr_t is near max_t
def compute_min_probability_if_among(min_t, max_t, max_p, curr_t) :
    result  = 2
    if min_t <= curr_t <= max_t:
        time_range      = (max_t-min_t)
        time_delta      = max_t-curr_t
        time_percentage = time_delta.total_seconds()/time_range.total_seconds()
        #print(f"Acceptable value! max_p is {max_p} -> {time_delta.total_seconds()} mapped in {time_range.total_seconds()} = {time_percentage}")
        # TODO Generate a min probability value with more accuracy
        result  = math.sqrt(time_percentage)
    return result

DETECTION_CONFIDENCE_RANGE  = [.65, 1]
MIN_CONFIDENCE              = .70

MAX_PEOPLE_COUNT        = 15
PEOPLE_DAY_PERCENTAGE   = {
        # min -max
    0   : [.4, .7],     # Monday
    1   : [.70, 1],     # Tuesday
    2   : [.4, .65],    # Wednesday
    3   : [.85, 1],     # Thursday
    4   : [0, .3],      # Friday
    5   : [0, 0],       # Saturday
    6   : [0, 0],       # Sunday
}

ENTRANCE_EXIT_DELAY_S   = 60    # FIXME Adjust this value
MOVEMENTS_DELAY_S       = 10    # FIXME Adjust this Value
ENTRANCE_PARAMS         = {
    "GET_START_TIME"        : lambda d : d.replace(hour=8, minute=0, second=0, microsecond=0),
    "GET_END_TIME"          : lambda d : d.replace(hour=10, minute=15, second=0, microsecond=0),
    "GET_MIN_PROBABILITY"   : lambda n : compute_min_probability_if_among(ENTRANCE_PARAMS["GET_START_TIME"](n),
                                                                          ENTRANCE_PARAMS["GET_END_TIME"](n),
                                                                          ENTRANCE_PARAMS["MAX_PROBABILITY"], n),
    "MAX_PROBABILITY"       : .8
}
EXIT_PARAMS             = {
    "GET_START_TIME"        : lambda d : d.replace(hour=17, minute=0, second=0, microsecond=0),
    "GET_END_TIME"          : lambda d : d.replace(hour=19, minute=0, second=0, microsecond=0),
    "GET_MIN_PROBABILITY"   : lambda n : compute_min_probability_if_among(EXIT_PARAMS["GET_START_TIME"](n),
                                                                          EXIT_PARAMS["GET_END_TIME"](n),
                                                                          EXIT_PARAMS["MAX_PROBABILITY"], n),
    "MAX_PROBABILITY"       : 1
}


ZONES_DESCRIPTORS   = {
    "Entrance"      : {
        "MAX_PEOPLE_COUNT"          : 12,
        "CONNECTED_AREAS"           : ["Break Area", "Meeting Area", "UX Area"],
        "ENTRANCE_WEIGHTS"    : {
                # min -max
            8   : [.3, .7],
            9   : [.3, .5],
            10  : [.3, .5],
            11  : [.5, .7],
            12  : [.3, .5],
            13  : [.5, .8],
            14  : [.5, .7],
            15  : [.3, .5],
            16  : [.4, .7],
            17  : [.7, .9],
            18  : [.7, 1]
        },
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .75],
            9   : [.3, .75],
            10  : [.5, .8],
            11  : [.65, .85],
            12  : [.65, .75],
            13  : [.3, .75],
            14  : [.3, .75],
            15  : [.4, .6],
            16  : [.4, .6],
            17  : [.4, .6],
            18  : [1, 1]
        },

        "current_people_count"  : 0
    },
    "Break Area"    : {
        "MAX_PEOPLE_COUNT"          : 15,
        "CONNECTED_AREAS"           : ["Entrance"],
        "ENTRANCE_WEIGHTS"    : {
                # min -max
            8   : [.3, .7],
            9   : [.3, .7],
            10  : [.3, .7],
            11  : [.5, .6],
            12  : [.7, .8],
            13  : [.7, .8],
            14  : [.8, .9],
            15  : [.8, .9],
            16  : [.4, .6],
            17  : [.3, .4],
            18  : [.2, .3]
        },
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.6, .8],
            9   : [.4, .7],
            10  : [.4, .7],
            11  : [.65, .85],
            12  : [.65, .75],
            13  : [.7, .9],
            14  : [.7, .9],
            15  : [.65, .75],
            16  : [.4, .9],
            17  : [.4, .7],
            18  : [.5, .8]
        },

        "current_people_count"  : 0
    },
    "Meeting Area"  : {
        "MAX_PEOPLE_COUNT"          : 8,
        "CONNECTED_AREAS"           : ["Entrance"],
        "ENTRANCE_WEIGHTS"    : {
                # min -max
            8   : [.3, .4],
            9   : [.3, .4],
            10  : [.3, .5],
            11  : [.6, .7],
            12  : [.5, .7],
            13  : [.5, .6],
            14  : [.3, .4],
            15  : [.4, .4],
            16  : [.6, .8],
            17  : [.3, .4],
            18  : [.2, .3]
        },
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .4],
            9   : [.3, .4],
            10  : [.5, .75],
            11  : [.6, .85],
            12  : [.7, .85],
            13  : [.4, .5],
            14  : [.3, .5],
            15  : [.5, .75],
            16  : [.6, .75],
            17  : [.4, .65],
            18  : [.4, .65]
        },

        "current_people_count"  : 0
    },
    "UX Area"   : {
        "MAX_PEOPLE_COUNT"          : 8,
        "CONNECTED_AREAS"           : ["Entrance"],
        "ENTRANCE_WEIGHTS"    : {
                # min -max
            8   : [.3, .4],
            9   : [.3, .4],
            10  : [.3, .5],
            11  : [.6, .7],
            12  : [.5, .7],
            13  : [.5, .6],
            14  : [.3, .4],
            15  : [.4, .4],
            16  : [.6, .8],
            17  : [.3, .4],
            18  : [.2, .3]
        },
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.6, .75],
            9   : [.7, .85],
            10  : [.8, .9],
            11  : [.8, .9],
            12  : [.8, .9],
            13  : [.8, .9],
            14  : [.3, .5],
            15  : [.3, .5],
            16  : [.7, .9],
            17  : [.8, .9],
            18  : [.4, .65]
        },

        "current_people_count"  : 0
    }
}