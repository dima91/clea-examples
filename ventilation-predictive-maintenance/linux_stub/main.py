
import asyncio, time, random
from datetime import datetime, timedelta
from argparse import ArgumentParser
from src.astarteClient import AstarteClient


def generate_random_value(curr, min, max, delta):
    next_v  = random.uniform(curr-delta, curr+delta)
    if next_v<min:
        next_v  = next_v+delta
    elif next_v>max:
        next_v  = next_v-delta

    #print (f'Next value is {next_v}')
    return next_v


async def simulator(astarte_client):

    LOOP_DELAY_S            = 5
    EVENTS_BASE_DELAY_S     = 60*5      # 5 minutes
    EVENTS_DELTA_S          = 40
    BASE_EVENT_DURATION_S   = 10.0
    EVENT_DURATION_DELTA_S  = 2.5

    DELTA_FLOW      = 0.1
    DELTA_POLLUTION = 2.5

    last_event_timestamp    = datetime.now()
    event_type              = None
    event_duration          = 0
    target_event_value      = 0

    curr_flow       = astarte_client.MAX_FLOW-DELTA_FLOW
    curr_pollution  = astarte_client.MIN_POLLUTION+DELTA_POLLUTION
    
    while True:
        time.sleep(LOOP_DELAY_S)

        # Checking if events should be created
        curr_timestamp      = datetime.now()
        delta_timestamps    = curr_timestamp-last_event_timestamp
        threshold_delta     = timedelta(seconds=EVENTS_BASE_DELAY_S+random.uniform(-EVENTS_DELTA_S, EVENTS_DELTA_S))

        if delta_timestamps>threshold_delta:
            print (f"New event: {delta_timestamps} > {threshold_delta}")
            # Creating the event
            last_event_timestamp    = curr_timestamp
            event_type              = random.randint(0,1)   # 0:flow, 1:pollution
            event_duration          = BASE_EVENT_DURATION_S + random.uniform(-EVENT_DURATION_DELTA_S,\
                                                                             EVENT_DURATION_DELTA_S)
            if event_type==0:
                # Flow event
                target_event_value  = random.uniform(astarte_client.MIN_FLOW+DELTA_FLOW,\
                                                     astarte_client.WARNING_FLOW-DELTA_FLOW)
                curr_flow           = target_event_value
            else:
                # Pollution event
                target_event_value  = random.uniform(astarte_client.WARNING_POLLUTION+DELTA_POLLUTION,\
                                                     astarte_client.MAX_POLLUTION-DELTA_POLLUTION)
                curr_pollution      = target_event_value
                
            print(f"event_type:{event_type}\ntarget_event_value:{target_event_value}\nevent_duration:{event_duration}")
        
        # Generating values for (eventually) existing event
        if event_type!=None:
            if event_type==0:
                print(f"New data for flow event, {delta_timestamps}")
                curr_flow       = generate_random_value(curr_flow, target_event_value-DELTA_FLOW,\
                                                target_event_value+DELTA_FLOW, DELTA_FLOW)
                curr_pollution  = generate_random_value(curr_pollution, astarte_client.MIN_POLLUTION,\
                                                    astarte_client.MIN_POLLUTION+DELTA_POLLUTION, DELTA_POLLUTION)
            else:
                print(f"New data for pollution event, {delta_timestamps}")
                curr_flow       = generate_random_value(curr_flow, astarte_client.MAX_FLOW-DELTA_FLOW,\
                                                            astarte_client.MAX_FLOW, DELTA_FLOW)
                curr_pollution  = generate_random_value(curr_pollution, target_event_value-DELTA_POLLUTION,\
                                                        target_event_value+DELTA_POLLUTION, DELTA_POLLUTION)

            # Recomputing delta_timestamps value
            delta_timestamps    = curr_timestamp-last_event_timestamp
            if delta_timestamps>timedelta(seconds=event_duration):
                # Clearing event
                print(f"Clearing event: d_ts{delta_timestamps}, {timedelta(seconds=event_duration)}, {event_duration}")
                event_type              = None
                event_duration          = 0
                target_event_value      = 0
                last_event_timestamp    = curr_timestamp

        else:
            curr_flow       = generate_random_value(curr_flow, astarte_client.MAX_FLOW-DELTA_FLOW,\
                                                astarte_client.MAX_FLOW, DELTA_FLOW)
            curr_pollution  = generate_random_value(curr_pollution, astarte_client.MIN_POLLUTION,\
                                                    astarte_client.MIN_POLLUTION+DELTA_POLLUTION, DELTA_POLLUTION)


        client.send_air_data(curr_flow, curr_pollution)


if __name__== "__main__" :
    parser  = ArgumentParser ()
    parser.add_argument ("-i", "--device-id", required=True)
    parser.add_argument ("-s", "--device-secret", required=True)
    parser.add_argument ("-u", "--api-base-url", required=True)
    parser.add_argument ("-n", "--realm-name", required=True)
    parser.add_argument ("-p", "--persistency-path", required=True)
    parser.add_argument ("-f", "--interfaces-folder", required=True)
    args    = parser.parse_args()

    loop    = asyncio.get_event_loop()

    # Building AstarteClient object with command line arguments
    client  = AstarteClient(args.device_id, args.realm_name, args.device_secret, args.api_base_url,
                            args.persistency_path, args.interfaces_folder, loop)
    client.connect()

    # Creating simulator task
    loop.create_task (simulator(client))

    loop.run_forever()