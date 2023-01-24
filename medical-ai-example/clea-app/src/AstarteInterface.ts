
import axios from 'axios';
import AstarteClient from './AstarteClient';
import { RoomDescriptor, Event } from './components/commons';
import moment from 'moment';
import _, { isArray, isObject, result } from 'lodash';

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
            console.error (`Cannot join room ${roomName}:`)
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
        }).then ((response) => response.data?.data["roomsIds"])
    }
    
    
    getRoomDetails (roomId : number) : Promise<RoomDescriptor> {
        const interfaceName = `it.unisi.atlas.RoomDescriptor`;
        const path          = `v1/${this.getRealm()}/devices/${this.getDeviceId()}/interfaces/${interfaceName}/${roomId}`;
        const requestUrl    = new URL (path, this.getAppengineUrl());

        //console.log (`Retrieving details for room ${roomId}`)

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
        let result_a    = await this.getLastRoomEvents (roomId, 1, undefined)
        return result_a[result_a.length-1]
    }


    /* Returns up to last "count" events published by the specific room "roomId", if specified.
        If "until" is specified, last "count" events will be retrieved from that time point, otherwise "until" will assume the current timestamp.
        Elements will be returned as an increasing timestamp sequence of Event objects
     */
    async getLastRoomEvents (roomId:number, count:number, until:moment.Moment|undefined) : Promise<Event[]> {
        if (until == undefined) {
            until   = moment()
        }

        const MS_IN_AN_HOUR = 86400000;
        const IT_THRESHOLD  = 20;

        const interfaceName     = `it.unisi.atlas.Event`;
        const path              = `v1/${this.getRealm()}/devices/${this.getDeviceId()}/interfaces/${interfaceName}/${roomId}`;
        const requestUrl        = new URL (path, this.getAppengineUrl());
        let timespan            = 0;
        let results : Event[]   = [];
        let itCount             = 0;

        while (results.length<count && itCount<IT_THRESHOLD) {
            let to      = moment (until.valueOf() - timespan)
            timespan += MS_IN_AN_HOUR
            let since   = moment (until.valueOf() - timespan)
            let query : Record<string, string>  = {"since":since.format("YYYY-MM-DDTHH:mm:ss"),
                                                    "to":to.format('YYYY-MM-DDTHH:mm:ss')};
            requestUrl.search                   = new URLSearchParams(query).toString()

            // console.log (`[${roomId}] New time range =>\t${query.since} - ${query.to}`)
            
            try {
                let response    = await axios.get (requestUrl.toString(), {
                    method  : "get",
                    headers : {
                        "Authorization" : `Bearer ${this.getAuthorizationToken()}`,
                        "content-type"  : "application/json;charset=UTF-8"
                    }
                })

                if (response.data.data!=undefined && isArray(response.data.data)) {
                    _.map (response.data.data, (item, idx) => {
                        item.timestamp  = moment(item.timestamp).valueOf()
                        item.roomId     = roomId
                        results.push (item)
                    })
                }
            } catch (err : any) {
                // console.error (`Catched an error: ${err.message}`)
            }

            itCount++
        }

        return results
    }


    /* Returns up to last "count" events published by the specific room "roomId", if specified.
        If "until" is specified, last "count" events will be retrieved from that time point, otherwise "until" will assume the current timestamp.
        Elements will be returned as an increasing timestamp sequence of Event objects
     */
    async getLastEvents (count:number, until:moment.Moment|undefined) : Promise<Event[]> {

        const roomsList         = await this.getRoomsList();

        let results : Event[]   = [];
        let itCount             = 0;
        let tmpResults          = [];

        for (let i in roomsList) {
            console.log (`i: ${i} -> ${roomsList[i]}`)
            tmpResults.push (this.getLastRoomEvents (Number(roomsList[i]), count, until))
        }

        for (let i in tmpResults) {
            let res = await tmpResults[i]
            results = results.concat (res)
        }

        results.sort ((a, b) => a.timestamp - b.timestamp)
        
        return results
    }
}

export default AstarteInterface;