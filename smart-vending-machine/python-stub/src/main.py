
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

    loop    = asyncio.get_event_loop()

    # Creating AstarteClient
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url, persistency_path, interfaces_folder, loop)
    client.connect()

    # Loading configuration
    config  = json.load(open(os.environ["CONFIG_FILE_PATH"]))

    # Creating Simulator
    simulator   = Simulator(config, client)
    s_task      = loop.create_task(simulator.run())

    loop.run_forever()


if __name__ == "__main__":
    main()