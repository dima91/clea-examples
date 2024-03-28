
import os, asyncio, time, random
from datetime import datetime, timedelta
from astarteClient import AstarteClient


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
    EVENTS_BASE_DELAY_S     = int(os.environ["EVENTS_DELAY_BASE_S"])
    EVENTS_DELTA_S          = int(os.environ["EVENTS_DELAY_DELTA_S"])
    BASE_EVENT_DURATION_S   = float(os.environ["EVENTS_DURATION_BASE_S"])
    EVENT_DURATION_DELTA_S  = float(os.environ["EVENTS_DURATION_DELTA_S"])

    DELTA_FLOW      = 0.1
    DELTA_POLLUTION = 2.5

    last_event_timestamp            = datetime.now()
    event_type                      = None
    event_duration                  = 0
    target_event_value              = 0
    last_wifi_update_timestamp      = datetime.now()
    last_cellular_update_timestamp  = datetime.now()

    curr_flow       = astarte_client.MAX_FLOW-DELTA_FLOW
    curr_pollution  = astarte_client.MIN_POLLUTION+DELTA_POLLUTION
    
    # Sending device info
    astarte_client.send_device_info()

    print("Running simulator loop..")
    while True:
        await asyncio.sleep(LOOP_DELAY_S)

        if astarte_client.ota_update_in_progress():
            print("Skipping simulator execution due to OTA update..")
            continue

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
            astarte_client.update_system_status(8, astarte_client.DEFAULT_AVAILABLE_MEM_BYTES-1866465)
            
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

                # Resetting tasks count and available memory
                astarte_client.update_system_status(astarte_client.DEFAULT_TASKS_COUNT, astarte_client.DEFAULT_AVAILABLE_MEM_BYTES)

        else:
            curr_flow       = generate_random_value(curr_flow, astarte_client.MAX_FLOW-DELTA_FLOW,\
                                                astarte_client.MAX_FLOW, DELTA_FLOW)
            curr_pollution  = generate_random_value(curr_pollution, astarte_client.MIN_POLLUTION,\
                                                    astarte_client.MIN_POLLUTION+DELTA_POLLUTION, DELTA_POLLUTION)
            
        # Checking if WiFi scan results should be updated
        if (curr_timestamp - last_wifi_update_timestamp) > timedelta(seconds=int(os.environ['WIFI_SCAN_RESULT_DELAY_UPDATE_S'])):
            astarte_client.update_wifi_scan_results()
            last_wifi_update_timestamp = curr_timestamp

        # Checking if cellular connection status should be updated
        if (curr_timestamp - last_cellular_update_timestamp) > timedelta(seconds=int(os.environ['CELLULAR_STATUS_DELAY_UPDATE_S'])):
            astarte_client.update_cellular_connection_status()
            last_cellular_update_timestamp = curr_timestamp


        client.send_air_data(curr_flow, curr_pollution)


if __name__== "__main__" :
    device_id           = os.environ["DEVICE_ID"]
    device_secret       = os.environ["DEVICE_SECRET"]
    api_base_url        = os.environ["API_BASE_URL"]
    realm_name          = os.environ["REALM_NAME"]
    persistency_path    = os.environ["PERSISTENCY_PATH"]
    interfaces_folder   = os.environ["INTERFACES_FOLDER"]

    

    loop    = asyncio.get_event_loop()

    # Building AstarteClient object with command line arguments
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url,
                            persistency_path, interfaces_folder, loop)
    client.connect(lambda : simulator(client))

    loop.run_forever()