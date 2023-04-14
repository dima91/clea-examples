
from astarteClient import AstarteClient
from localDB import LocalDB
from simulator import CoffeeMachineSimulator

import os, asyncio, time, random


def main():
    device_id           = os.environ["DEVICE_ID"]
    device_secret       = os.environ["DEVICE_SECRET"]
    api_base_url        = os.environ["API_BASE_URL"]
    realm_name          = os.environ["REALM_NAME"]
    persistency_path    = os.environ["PERSISTENCY_PATH"]
    interfaces_folder   = os.environ["INTERFACES_FOLDER"]
    country             = os.environ["COUNTRY"]

    local_db_path       = "/data/local.db"

    loop    = asyncio.get_event_loop()

    # Building AstarteClient object with command line arguments
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url,
                            persistency_path, interfaces_folder, loop)
    client.connect()

    # Creating LocalDB object
    local_db    = LocalDB(local_db_path)

    # Setting up coffe machine simulator
    simulator   = CoffeeMachineSimulator(client, local_db, country)
    simulator.set_people_count(12)          # FIXME
    simulator.set_container_capacity(27)    # FIXME
    simulator.set_water_capacity(14)        # FIXME

    # Creating simulator task
    loop.create_task (simulator.run())

    loop.run_forever()

if __name__ == "__main__":
    main()

