
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
        result  = time_percentage
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

ENTRANCE_EXIT_DELAY_S   = 10
#ENTRANCE_EXIT_DELAY_S   = 300   # FIXME Adjust this value!
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
        "MAX_PEOPLE_COUNT"      : 10,
        "CONNECTED_AREAS"       : ["Break Area", "Meeting Area", "UX Area"],
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .75],
            9   : [.3, .75],
            10  : [.3, .75],
            11  : [.3, .75],
            12  : [.3, .75],
            13  : [.3, .75],
            14  : [.3, .75],
            15  : [.3, .75],
            16  : [.3, .75],
            17  : [.3, .75],
            18  : [.3, .75],
        },

        "current_people_count"  : 0
    },
    "Break Area"    : {
        "MAX_PEOPLE_COUNT"      : 10,
        "CONNECTED_AREAS"       : ["Entrance"],
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .75],
            9   : [.3, .75],
            10  : [.3, .75],
            11  : [.3, .75],
            12  : [.3, .75],
            13  : [.3, .75],
            14  : [.3, .75],
            15  : [.3, .75],
            16  : [.3, .75],
            17  : [.3, .75],
            18  : [.3, .75],
        },

        "current_people_count"  : 0
    },
    "Meeting Area"  : {
        "MAX_PEOPLE_COUNT"      : 10,
        "CONNECTED_AREAS"       : ["Entrance"],
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .75],
            9   : [.3, .75],
            10  : [.3, .75],
            11  : [.3, .75],
            12  : [.3, .75],
            13  : [.3, .75],
            14  : [.3, .75],
            15  : [.3, .75],
            16  : [.3, .75],
            17  : [.3, .75],
            18  : [.3, .75],
        },

        "current_people_count"  : 0
    },
    "UX Area"   : {
        "MAX_PEOPLE_COUNT"      : 10,
        "CONNECTED_AREAS"       : ["Entrance"],
        "EXIT_PROBABILITIES"    : {
                # min -max
            8   : [.3, .75],
            9   : [.3, .75],
            10  : [.3, .75],
            11  : [.3, .75],
            12  : [.3, .75],
            13  : [.3, .75],
            14  : [.3, .75],
            15  : [.3, .75],
            16  : [.3, .75],
            17  : [.3, .75],
            18  : [.3, .75],
        },

        "current_people_count"  : 0
    }
}