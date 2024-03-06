import os, glob, json, utils, time
from datetime import datetime
from astarte.device import DeviceMqtt


class AstarteClient :

    # Astarte interfaces
    __EVENT_INTERFACE                       = "it.unisi.atlas.Event"
    __ROOM_DESCRIPTOR_INTERFACE             = "it.unisi.atlas.RoomDescriptor"
    __ROOMS_MANAGER_DESCRIPTOR_INTERFACE    = "it.unisi.atlas.RoomsManagerDescriptor"

    __device        = None
    __device_id     = None
    __api_base_url  = None
    __realm         = None
    __loop          = None


    def __init__(self, device_id, realm_name, credentials_secret, api_base_url, persistency_path, interfaces_folder, loop) -> None:

        self.__device_id        = device_id
        self.__api_base_url     = api_base_url
        self.__realm            = realm_name
        self.__loop             = loop

        if not os.path.exists(persistency_path) :
            print ("Directory at path "+persistency_path+" does not exists.\nCreating it...")
            os.mkdir (persistency_path)
        elif not os.path.isdir (persistency_path) :
            error_message   = f"File at path {persistency_path} is not a directory"
            print (error_message)
            raise Exception (error_message)

        self.__device   = DeviceMqtt (device_id=device_id,
                                      realm=realm_name,
                                      credentials_secret=credentials_secret,
                                      pairing_base_url=f"{api_base_url}/pairing",
                                      persistency_dir=persistency_path
                                      )
        self.__device.set_events_callbacks(on_connected=self.__connection_cb, on_data_received=self.__data_cb, on_disconnected=self.__disconnecton_cb, loop=self.__loop)

        # Adding used interfaces
        for filename in glob.iglob(f'{interfaces_folder}/*.json'):
            if os.path.isfile(filename) :
                print (f"Loading interface in {filename}...")
                self.__device.add_interface_from_json (json.load(open(filename)))
            else:
                print (f"File {filename} is not file!")


    def __connection_cb(self, dvc) :
        print ('================\nDevice connected\n================\n\n')

    def __disconnecton_cb(self, dvc, code) :
        print ('===================\nDevice disconnected\n===================\n\n')
    
    def __data_cb(self, astarte_device, interface, path, data) :
        print ("Received server data")


    ##### ================================ #####


    def connect(self):
        self.__device.connect()
        time.sleep(1)
    
    
    def is_connected(self) :
        return self.__device.is_connected()
    

    def publish_rooms_identifiers(self, rooms_id) -> None:
        self.__device.send(self.__ROOMS_MANAGER_DESCRIPTOR_INTERFACE, "/roomsIds", rooms_id)


    def publish_room_descriptor(self, room_id:int, patient_id:int, diagnosis:str, hospitalization_date:datetime,
                                release_date:datetime) -> None:
        self.__device.send(self.__ROOM_DESCRIPTOR_INTERFACE, f"/r_{room_id}/patientId", patient_id)
        self.__device.send(self.__ROOM_DESCRIPTOR_INTERFACE, f"/r_{room_id}/diagnosis", diagnosis)
        self.__device.send(self.__ROOM_DESCRIPTOR_INTERFACE, f"/r_{room_id}/patientHospitalizationDate", hospitalization_date)
        self.__device.send(self.__ROOM_DESCRIPTOR_INTERFACE, f"/r_{room_id}/patientReleaseDate", release_date)

    
    def publish_event(self, event_type:utils.EventType, confidence:float, init_frame_content:bytes, init_frame_url:str,
                      room_id:int) -> None:
        payload = {
            "eventType"     : event_type.value,
            "confidence"    : float(confidence),
            "roomId"        : room_id,
            "initFrameContent"  : b'',
            "initFrameURL"  : ''
        }
        if init_frame_content:
            payload['initFrameContent'] = init_frame_content
        if init_frame_url:
            payload['initFrameURL']     = init_frame_url
        
        self.__device.send_aggregate(self.__EVENT_INTERFACE, f"/r_{room_id}", payload)
