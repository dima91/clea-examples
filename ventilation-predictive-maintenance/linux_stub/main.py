
import os, asyncio, json, datetime, time
from argparse import ArgumentParser
from src.astarteClient import AstarteClient


async def coroutine():
    time.sleep(5.300)
    print(__name__)


async def main(astarte_client):

    astarte_client.connect()
    
    while True:
        time.sleep(2.5)
        print (f"Connected? {client.is_connected()}")
        client.send_air_data(1.0, 25.0, 0.0)


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

    client  = AstarteClient(args.device_id, args.realm_name, args.device_secret, args.api_base_url,
                            args.persistency_path, args.interfaces_folder, loop)

    loop.create_task (main(client))

    print ("Running loop..")
    loop.run_forever()