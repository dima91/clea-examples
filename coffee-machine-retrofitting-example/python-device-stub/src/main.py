
from astarteClient import AstarteClient, ContainerStatus, WaterStatus
from localDB import LocalDB

import os, asyncio, time, random


async def simulator(client:AstarteClient, db:LocalDB):
    while True:
        #TODO
        pass


def main():
    device_id           = os.environ["DEVICE_ID"]
    device_secret       = os.environ["DEVICE_SECRET"]
    api_base_url        = os.environ["API_BASE_URL"]
    realm_name          = os.environ["REALM_NAME"]
    persistency_path    = os.environ["PERSISTENCY_PATH"]
    interfaces_folder   = os.environ["INTERFACES_FOLDER"]

    local_db_path       = "/data/local.db"

    loop    = asyncio.get_event_loop()

    # Building AstarteClient object with command line arguments
    client  = AstarteClient(device_id, realm_name, device_secret, api_base_url,
                            persistency_path, interfaces_folder, loop)
    client.connect()

    # Creating LocalDB object
    local_db    = LocalDB(local_db_path)

    # Creating simulator task
    loop.create_task (simulator(client, local_db))

    loop.run_forever()

if __name__ == "__main__":
    main()

