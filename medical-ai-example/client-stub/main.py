
# IHrmuoV6TumaVNGHu42Gvw
# vllgDa1OZxsgh8andIcixoXQHc/GezwBmIRmrct9cYk=

import os, asyncio, base64, requests, json, datetime
from astarte import device
from argparse import ArgumentParser


class App:
    
    def __init__(self, args) -> None:
        print (f"{args}=")

        self.args               = args
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

        print ("Connecting to {}@{} as {} ({})".format (self.args.astarte_pairing_url, self.args.realm_name,
                                                        self.args.device_id, self.args.device_secret))

        # Creating a Device object
        self.astarte_device = device.Device(self.args.device_id, self.args.realm_name,
                                                    self.args.device_secret, self.args.astarte_pairing_url,
                                                    self.persistency_path,
                                                    loop=self.astarte_loop)

        # Setting up callbacks
        self.astarte_device.on_connected                = self.astarte_conection_cb
        self.astarte_device.on_disconnected             = self.astarte_disconnection_cb
        self.astarte_device.on_data_received            = self.astarte_data_cb
        self.astarte_device.on_aggregate_data_received  = self.astarte_aggr_data_cb

        # Adding interfaces
        self.add_interfaces ()




    def add_interfaces (self) -> None :
        # Event interface
        self.interface_name     = "it.unisi.atlas.Event5"   # FIXME The interface name should be "it.unisi.atlas.Event"
        interface_descriptor    = {
            "interface_name": self.interface_name,
            "version_major": 0,
            "version_minor": 1,
            "type": "datastream",
            "ownership": "device",
            "aggregation": "object",
            "mappings": [
                {
                    "endpoint": "/%{roomId}/confidence",
                    "type": "double"
                },
                {
                    "endpoint": "/%{roomId}/eventType",
                    "type": "string"
                },
                {
                    "endpoint": "/%{roomId}/initFrameContent",
                    "type": "stringarray"
                },
                {
                    "endpoint": "/%{roomId}/initFrameURL",
                    "type": "string"
                }
            ]
        }
        self.astarte_device.add_interface (interface_descriptor)

        # RoomsManagerDescriptor interface
        interface_descriptor    = {
            "interface_name": "it.unisi.atlas.RoomsManagerDescriptor",
            "version_major": 0,
            "version_minor": 1,
            "type": "properties",
            "ownership": "device",
            "mappings": [
                {
                    "endpoint": "/roomsIds",
                    "type": "integerarray",
                    "description": "List of rooms IDs handled by the board"
                }
            ]
        }
        self.astarte_device.add_interface (interface_descriptor)

        # RoomDescriptor interface
        interface_descriptor    = {
            "interface_name": "it.unisi.atlas.RoomDescriptor",
            "version_major": 0,
            "version_minor": 1,
            "type": "properties",
            "ownership": "device",
            "mappings": [
                {
                    "endpoint": "/%{roomId}/patientId",
                    "type": "integer",
                    "description": "Patient identifier"
                },
                {
                    "endpoint": "/%{roomId}/diagnosis",
                    "type": "string",
                    "description": "Brief diagnosis description"
                },
                {
                    "endpoint": "/%{roomId}/patientHospitalizationDate",
                    "type": "datetime"
                },
                {
                    "endpoint": "/%{roomId}/patientReleaseDate",
                    "type": "datetime",
                    "description": "Expected release date"
                }
            ]
        }
        self.astarte_device.add_interface (interface_descriptor)





    def run (self) -> None:
        self.astarte_device.connect()
        self.astarte_loop.run_forever()


    def publish_image (self) -> None:
        #TODO
        files   = {
                    'file': self.f
                }
        res_p   = requests.post ("https://tmpfiles.org/api/v1/upload", files=files)
        j_res   = json.loads (res_p.text)
        print (j_res)
        # res_g   = requests.get (j_res["data"]["url"])
        # print (res_g.text)

        return "https://google.com"
        

    def astarte_conection_cb (self, dvc) -> None:
        print ('\n================\nDevice connected\n================\n\n')

        # TODO Publishing rooms information
        rs_info = [7, 12, 14, 20, 25]
        self.astarte_device.send ("it.unisi.atlas.RoomsManagerDescriptor", f'/roomsIds', rs_info)

        rds_info    = [
            {
                "patientId" : 373892,
                "diagnosis" : "mal di gola",
                "patientHospitalizationDate" : 1672550400,
                "patientReleaseDate" : 1672567200
            },
            {
                "patientId" : 37386,
                "diagnosis" : "mal di gola",
                "patientHospitalizationDate" : 1672550400,
                "patientReleaseDate" : 1672567200
            },
            {
                "patientId" : 32490,
                "diagnosis" : "mal di gola",
                "patientHospitalizationDate" : 1672550400,
                "patientReleaseDate" : 1672567200
            },
            {
                "patientId" : 35567,
                "diagnosis" : "mal di gola",
                "patientHospitalizationDate" : 1672550400,
                "patientReleaseDate" : 1672567200
            },
            {
                "patientId" : 38769,
                "diagnosis" : "mal di gola",
                "patientHospitalizationDate" : 1672550400,
                "patientReleaseDate" : 1672567200
            }
        ]
        idx=0
        for i in rds_info :
            print (i)
            for k in i.keys() :
                print(k)
                if k == "patientHospitalizationDate" :
                    self.astarte_device.send ("it.unisi.atlas.RoomDescriptor", f'/{rs_info[idx]}/{k}', datetime.datetime.fromtimestamp(i[k]))
                else :
                    self.astarte_device.send ("it.unisi.atlas.RoomDescriptor", f'/{rs_info[idx]}/{k}', i[k])
            idx = idx +1
        
        while True :
            print ("\n\n")
            
            i   = int(input("Type the room identifier:  "))
            t   = input("Type the event type:  ")
            c   = input("Type the confidence (if needed):  ")

            try :
                c   = float(c)
            except ValueError as e:
                c   = -1

            # Building Astarte data
            a_data  = {}
            if c != -1 :
                a_data["confidence"]    = c
            a_data["eventType"]     = t
            a_data["initFrameURL"]  = t
            
            self.astarte_device.send_aggregate (self.interface_name, f'/{i}', a_data)

    def astarte_disconnection_cb (self, dvc) -> None:
        print ('\n================\nDevice disconnected\n================\n\n')
        pass


    def astarte_data_cb (self, data) -> None:
        print ('\n================\nNew server data\n================\n\n')
        pass


    def astarte_aggr_data_cb (self, data) -> None:
        print ('\n================\nNew server aggregated data\n================\n\n')
        pass




parser  = ArgumentParser ()
parser.add_argument ("-i", "--device-id", required=True)
parser.add_argument ("-s", "--device-secret", required=True)
parser.add_argument ("-u", "--astarte-pairing-url", required=True)
parser.add_argument ("-n", "--realm-name", required=True)
args    = parser.parse_args()


app     = App (args)

try :
    app.run ()
except BaseException as e:
    print ('\nCatched this exception:\n{}\n'.format(e))