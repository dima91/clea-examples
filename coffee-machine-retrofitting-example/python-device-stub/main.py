
import argparse
import os
import asyncio
import redis
from astarte import device


class MainApp :
    
    def __init__(self, args) -> None:
        self.params = args

        # Crating REDIS connection
        pool        = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redis  = redis.Redis(connection_pool=pool)

        # Loading counters
        try :
            self.params.short_coffee    = int(self.redis.get ('short_coffee'))
        except BaseException:
            self.params.short_coffee    = 0
            self.redis.set ('short_coffee', self.params.short_coffee)

        try :
            self.params.long_coffee     = int(self.redis.get ('long_coffee'))
        except BaseException :
            self.params.long_coffee     = 0
            self.redis.set ('long_coffee', self.params.long_coffee)


        print (f'{self.params=}')


        # Initializing Astarte client
        self.persistency_dir    = "astarte_persistency.d"
        self.persistency_path   = os.path.curdir+'/'+self.persistency_dir

        self.astarte_loop       = asyncio.get_event_loop ()

        # Checking existence of persistence directory
        if not os.path.exists(self.persistency_path) :
            print ("Directory at path "+self.persistency_path+" does not exists.\nCreating it...")
            os.mkdir (self.persistency_path)
        elif not os.path.isdir (self.persistency_path) :
            error_message   = "File at path "+self.persistency_path+" is not a directory"
            print (error_message)
            raise Exception (error_message)

        print ("Connecting to {}@{} as {} ({})".format (self.params.astarte_pairing_url, self.params.realm_name,
                                                        self.params.device_id, self.params.device_secret))

        # Creating a Device object
        self.astarte_device = device.Device(self.params.device_id, self.params.realm_name,
                                                    self.params.device_secret, self.params.astarte_pairing_url,
                                                    self.persistency_path,
                                                    loop=self.astarte_loop)

        # Setting up callbacks
        self.astarte_device.on_connected                = self.astarte_connection_cb
        self.astarte_device.on_disconnected             = self.astarte_disconnection_cb
        self.astarte_device.on_data_received            = self.astarte_data_cb
        self.astarte_device.on_aggregate_data_received  = self.astarte_aggr_data_cb

        # Defining and adding "ai.clea.examples.machine.Status" interface
        self.status_interface_name          = "ai.clea.examples.machine.Status"
        self.status_interface_descriptor    = {
            "interface_name"    : self.status_interface_name,
            "version_major": 0,
            "version_minor": 1, 
            "type": "datastream",
            "ownership": "device",
            "mappings" : [
                {
                    "endpoint": "/longCoffee",
                    "type": "integer",
                    "database_retention_policy": "use_ttl",
                    "database_retention_ttl": 31536000
                },
                {
                    "endpoint": "/shortCoffee",
                    "type": "integer",
                    "database_retention_policy": "use_ttl",
                    "database_retention_ttl": 31536000
                }
            ]
        }
        self.astarte_device.add_interface (self.status_interface_descriptor)

        # Defining and adding "ai.clea.examples.machine.Counters" interface
        self.counter_interface_name         = "ai.clea.examples.machine.Counters"
        self.counter_interface_descriptor   = {
            "interface_name": self.counter_interface_name,
            "version_major": 0,
            "version_minor": 1,
            "type": "datastream",
            "ownership": "device",
            "mappings": [
                {
                    "endpoint": "/containerStatus",
                    "type": "string",
                    "database_retention_policy": "use_ttl",
                    "database_retention_ttl": 31536000,
                    "description": "Event code. Possible values [ 'CONTAINER_OFF_ALARM_EVENT' | 'CONTAINER_OPEN_ALARM_EVENT' | 'CONTAINER_FULL_ALARM_EVENT' ]"
                },
                {
                    "endpoint": "/waterStatus",
                    "type": "string",
                    "database_retention_policy": "use_ttl",
                    "database_retention_ttl": 31536000,
                    "description": "Event code. Possible values [ 'WATER_OFF_ALARM_EVENT' | 'WATER_EMPTY_ALARM_EVENT' | 'WATER_OPEN_ALARM_EVENT' ]"
                }
            ]
        }
        self.astarte_device.add_interface (self.counter_interface_descriptor)

    
    def run (self) -> None:
        self.astarte_device.connect()
        self.astarte_loop.run_forever()


    def astarte_connection_cb (self, dvc) :
        #print ("astarte_connection_cb")

        while True:
            inp = input ("\nType something: ")

            if inp == "1":
                # Increasing short coffe
                print ("sc++")
                self.params.short_coffee    = self.params.short_coffee+1
                self.redis.set ('short_coffee', self.params.short_coffee)
                self.astarte_device.send (self.counter_interface_name, "/shortCoffee", self.params.short_coffee)

            
            elif inp == "2":
                # Increasing long coffe
                print ("lc++")
                self.params.long_coffee     = self.params.long_coffee+1
                self.redis.set ('long_coffee', self.params.long_coffee)
                self.astarte_device.send (self.counter_interface_name, "/longCoffee", self.params.long_coffee)

            elif inp == "3":
                # Toggling water container
                print ("wc_toggle")
                self.params.water_container = not self.params.water_container
                if self.params.water_container :
                    self.astarte_device.send (self.status_interface_name, "/waterStatus", "WATER_EMPTY_ALARM_EVENT")
                else :
                    self.astarte_device.send (self.status_interface_name, "/waterStatus", "WATER_OFF_ALARM_EVENT")

            elif inp == "4":
                # Toggling trash container
                print ("tc_toggle")
                self.params.trash_container = not self.params.trash_container
                if self.params.trash_container :
                    self.astarte_device.send (self.status_interface_name, "/containerStatus", "CONTAINER_FULL_ALARM_EVENT")
                else :
                    self.astarte_device.send (self.status_interface_name, "/containerStatus", "CONTAINER_OFF_ALARM_EVENT")



    def astarte_disconnection_cb (self) :
        print ("astarte_disconnection_cb")


    def astarte_data_cb (self) :
        print ("astarte_data_cb")


    def astarte_aggr_data_cb (self) :
        print ("astarte_aggr_data_cb")


################################################################################
################################################################################


def main () :
    parser = argparse.ArgumentParser ()
    parser.add_argument ("-i", "--device-id", required=True)
    parser.add_argument ("-s", "--device-secret", required=True)
    parser.add_argument ("-u", "--astarte-pairing-url", required=True)
    parser.add_argument ("-n", "--realm-name", required=True)
    #parser.add_argument ("-sc", "--short-coffee", required=True, type=int)
    #parser.add_argument ("-lc", "--long-coffee", required=True, type=int)
    args                    = parser.parse_args()
    args.water_container    = False
    args.trash_container    = False
    app                     = MainApp (args)

    try :
        app.run ()
    except BaseException as e :
        print ('\nCatched this exception:\n', e, '\n')
        print ("\n\n")
        print ("short coffee", args.short_coffee)
        print ("long coffee", args.long_coffee)


if __name__ == "__main__"   :
    main()