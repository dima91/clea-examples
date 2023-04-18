
import os, asyncio, json
from astarteClient import AstarteClient
from simulator import Simulator


def main() -> None:

    device_id           = os.environ["DEVICE_ID"]
    device_secret       = os.environ["DEVICE_SECRET"]
    api_base_url        = os.environ["API_BASE_URL"]
    realm_name          = os.environ["REALM_NAME"]
    persistency_path    = os.environ["PERSISTENCY_PATH"]
    interfaces_folder   = os.environ["INTERFACES_FOLDER"]

    loop                = asyncio.get_event_loop()

    # Creating AstarteClient
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url, persistency_path, interfaces_folder, loop)
    client.connect()

    # Loading and publishing scene settings
    scene_settings      = json.load(open("scene-settings.json"))
    client.publish_scene_settings(scene_settings)
    client.publish_update_interval(int(os.environ["UPDATE_INTERVAL_MS"]))

    # Creating Simulator
    simulator   = Simulator(client, loop, int(os.environ["UPDATE_INTERVAL_MS"]), scene_settings, os.environ["COUNTRY"])
    loop.create_task(simulator.run())

    loop.run_forever()




if __name__ == "__main__" :
    main()