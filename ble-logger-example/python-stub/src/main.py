
import os, asyncio, json
from astarte_client import AstarteClient
from simulator import Simulator


def main():
    device_id           = os.environ["DEVICE_ID"]
    device_secret       = os.environ["DEVICE_SECRET"]
    api_base_url        = os.environ["API_BASE_URL"]
    realm_name          = os.environ["REALM_NAME"]
    persistency_path    = os.environ["PERSISTENCY_PATH"]
    interfaces_folder   = os.environ["INTERFACES_FOLDER"]

    loop        = asyncio.get_event_loop()
    simulator   = None

    # Wrapping simulator execution in a lambda
    on_connection_lambda    = lambda : loop.create_task(simulator.run())

    # Loading configuration
    config  = json.load(open(os.environ["CONFIG_FILE_PATH"]))

    # Creating AstarteClient
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url, persistency_path, interfaces_folder,
                            loop, on_connection_lambda)
    client.connect()

    # Creating Simulator
    simulator   = Simulator(config, client, os.environ['TZ'])

    loop.run_forever()


if __name__ == "__main__":
    main()