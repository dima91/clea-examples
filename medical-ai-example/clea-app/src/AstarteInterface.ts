
import axios from 'axios';
import AstarteClient from './AstarteClient';
import { RoomDescriptor, Event, stringToPatientStatus } from './components/commons';
import moment from 'moment';
import { isArray } from 'lodash';

type AstarteInterfaceProps = {
    astarteUrl: URL;
    realm: string;
    token: string;
    deviceId: string;
}

class AstarteInterface {
    
    private astarteClient : AstarteClient;
    private config : AstarteInterfaceProps
    private room : String | null


    constructor (config : AstarteInterfaceProps) {
        this.config         = config
        this.astarteClient  = new AstarteClient (this.config)
        this.room           = null
    }


    async getIntrospection () {
        return this.astarteClient.getIntrospection()
    }

    async getDeviceInformation () {
        return this.astarteClient.getDeviceInformation()
    }

    async registerIncomingDataTrigger (eventHandler:(evt:any) => void, interface_name:string, value_match_operator:String, match_path:String) {
        const salt          = Math.floor(Math.random() * 10000);
        const roomName      = `room_${this.astarteClient.getDeviceId()}_${salt}`;
        const introspection = await this.getIntrospection()

        return this.astarteClient
        .joinRoom (roomName)
        .then (() => {
            this.astarteClient.listenForEvents(roomName, eventHandler);

            if (introspection == null)
                throw "Cannot get introspection"

            const deviceDataTriggerPayload = {
                name: `dataTrigger-${this.getDeviceId()}`,
                device_id: this.getDeviceId(),
                simple_trigger: {
                    type: "data_trigger",
                    on: "incoming_data",
                    interface_name: interface_name,
                    interface_major: introspection[interface_name].major,
                    value_match_operator: value_match_operator,
                     match_path: match_path
                },
            }
            
            return this.astarteClient
            .registerVolatileTrigger(roomName, deviceDataTriggerPayload)
            .then((err) => roomName)
            .catch((err) => {
                console.error(`Couldn't watch for deviceData events:`);
                console.error (err)
            });
        })
        .catch ((err) => {
            console.error (`Cannot join toom ${roomName}:`)
            console.error (err)
        })
    }

    getRealm() : String {
        return this.astarteClient.getRealm();
    }
    getDeviceId() : String {
        return this.astarteClient.getDeviceId()
    }
    getAppengineUrl() : URL {
        return this.astarteClient.getAppEngineUrl()
    }
    getAuthorizationToken() : string {
        return this.config.token
    }


    // ================================================================================
    // ================================================================================
    // App related methods


    getRoomsList () : Promise<Number[]> {
        const interfaceName = "it.unisi.atlas.RoomsManagerDescriptor";
        const path          = `v1/${this.getRealm()}/devices/${this.getDeviceId()}/interfaces/${interfaceName}`;
        const requestUrl    = new URL (path, this.getAppengineUrl());
        
        return axios ({
            method  : "get",
            url     : requestUrl.toString(),
            headers : {
                "Authorization" : `Bearer ${this.getAuthorizationToken()}`,
                "content-type"  : "application/json;charset=UTF-8"
            }
        }).then ((response) => response.data?.data)
    }
    
    
    getRoomDetails (roomId : number) : Promise<RoomDescriptor> {
        const interfaceName = `it.unisi.atlas.RoomDescriptor`;
        const path          = `v1/${this.getRealm()}/devices/${this.getDeviceId()}/interfaces/${interfaceName}/${roomId}`;
        const requestUrl    = new URL (path, this.getAppengineUrl());

        console.log (`Retrieving details for room ${roomId}`)

        return axios ({
            method  : "get",
            url     : requestUrl.toString(),
            headers : {
                "Authorization" : `Bearer ${this.getAuthorizationToken()}`,
                "content-type"  : "application/json;charset=UTF-8"
            }
        }).then (async (response) => {
            let currRoom    = response.data.data

            if(currRoom == undefined)
                throw `[getRoomDetails] Wrong room identifier (${roomId})`

            // Geting current patient status
            let lastEvent   = await this.getLastEvent (roomId)

            return {
                roomId                      : roomId,
                patientId                   : currRoom.patientId,
                diagnosis                   : currRoom.diagnosis,
                currentEvent                : lastEvent,
                patientHospitalizationDate  : moment(currRoom.patientHospitalizationDate).valueOf(),
                patientReleaseDate          : moment(currRoom.patientReleaseDate).valueOf()
            }
        })
        .catch ((err) => {
            console.log (`Error`)
            console.log (err)
            throw err
        })
    }


    async getLastEvent (roomId:number) : Promise<Event> {
        
        const MS_IN_AN_HOUR = 86400000;
        const IT_THRESHOLD     = 10;

        const interfaceName = `it.unisi.atlas.Event5`;
        const path          = `v1/${this.getRealm()}/devices/${this.getDeviceId()}/interfaces/${interfaceName}/${roomId}`;
        const requestUrl    = new URL (path, this.getAppengineUrl());
        const currTime      = moment().valueOf()
        let timespan        = 0;
        let result          = undefined;
        let itCount         = 0;

        while (result == undefined) {

            timespan += MS_IN_AN_HOUR
            let since   = moment (currTime - timespan)
            let query : Record<string, string>  = {"since":since.format("YYYY-MM-DDTHH:mm:ss")};
            requestUrl.search                   = new URLSearchParams(query).toString()

            console.log (`New time limit: ${query.since}`)
            

            // Retrieving data in the current timespan
            try {
                let response    = await axios.get (requestUrl.toString(), {
                    method  : "get",
                    headers : {
                        "Authorization" : `Bearer ${this.getAuthorizationToken()}`,
                        "content-type"  : "application/json;charset=UTF-8"
                    }
                })

                if (response.data.data != undefined && isArray (response.data.data) && response.data.data.length > 0) {
                    result  = response.data.data[response.data.data.length-1]
                }
                    
            } catch (err) {
                if (++itCount > IT_THRESHOLD)
                    throw undefined;
            }
        }

        result.timestamp    = moment(result.timestamp).valueOf()
        result.roomId       = roomId
        return result;
    }


    async getLastEvents (roomId:number | undefined, count:number) : Promise<Event[]> {
        return []
    }
}

export default AstarteInterface;