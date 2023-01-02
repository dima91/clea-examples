
import axios from 'axios';
import AstarteClient from './AstarteClient';

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


    async getRoomsList () : Promise<Number[]> {
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


    //async getLastEvents (count) : Promise<> {}
}

export default AstarteInterface;