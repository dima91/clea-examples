
import axios, { Method } from 'axios';
import AstarteClient from './AstarteClient';
import moment from 'moment';
import { isArray, isObject} from 'lodash';
import _ from 'lodash';
import { Console } from 'console';

type AstarteInterfaceProps = {
    astarteUrl: URL;
    realm: string;
    token: string;
    deviceId: string;
}

type CameraDataParameters = {
    deviceId: string;
    sinceAfter?: string;
    since?: Date;
    to?: Date;
    limit?: number;
};

type MultipleCameraDataParameters = {
    deviceId: string;
    since: Date;
    to: Date;
};




class AstarteInterface {
    
    private astarteClient : AstarteClient;
    private config : AstarteInterfaceProps
    private room : String | null

    // TODO Astarte interfaces
    private people_counter_interface    = "ai.clea.examples.PeopleCounter"
    private scene_settings_interface    = "ai.clea.examples.SceneSettings"


    constructor (config : AstarteInterfaceProps) {
        this.config         = config
        this.astarteClient  = new AstarteClient (this.config)
        this.room           = null
    }


    async get_introspection () {
        return this.astarteClient.getIntrospection()
    }

    async get_device_Information () {
        return this.astarteClient.getDeviceInformation()
    }

    async register_incoming_data_trigger (event_handler:(evt:any) => void, interface_name:string, value_match_operator:String, match_path:String) {
        const salt          = Math.floor(Math.random() * 10000);
        const roomName      = `room_${this.astarteClient.getDeviceId()}_${salt}`;
        const introspection = await this.get_introspection()

        return this.astarteClient
        .joinRoom (roomName)
        .then (() => {
            this.astarteClient.listenForEvents(roomName, event_handler);

            if (introspection == null)
                throw "Cannot get introspection"

            const deviceDataTriggerPayload = {
                name: `dataTrigger-${this.get_device_id()}`,
                device_id: this.get_device_id(),
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

    get_realm() : String {
        return this.astarteClient.getRealm();
    }
    get_device_id() : String {
        return this.astarteClient.getDeviceId()
    }
    get_appengine_url() : URL {
        return this.astarteClient.getAppEngineUrl()
    }
    get_authorization_token() : string {
        return this.config.token
    }

    build_request(method:Method, request_url:URL, query:any, payload:any){
        let request_params  = {
            method  : method,
            headers : {
                "Authorization" : `Bearer ${this.astarteClient.getAuthorizationToken()}`,
                "Content-Type"  : "application/json;charset=UTF-8"
            },
            data    : JSON.stringify({data:payload})
        }
        if (query)
            request_url.search  = new URLSearchParams(query).toString()
        
        return axios(request_url.toString(), request_params)
    }

    build_path(interface_name:string) : string {
        return `v1/${this.get_realm()}/devices/${this.get_device_id()}/interfaces/${interface_name}`
    }


    // ================================================================================
    // ================================================================================


    private ITERATIONS_THRESHOLD    = 20
    private async get_last_datastream_items(path:string, items_count:number, until:moment.Moment|undefined=undefined,
                                            iterations_threshold:number= this.ITERATIONS_THRESHOLD) {
        if (until == undefined) {
            until   = moment()
        }

        const MS_IN_AN_HOUR     = 86400000;
        const request_url       = new URL(path, this.get_appengine_url())
        let iterations_count    = 0
        let results:any[]             = []
        let timespan            = 0

        while (results.length<items_count && iterations_count<iterations_threshold) {
            let to              = moment (until.valueOf() - timespan)
            timespan            += MS_IN_AN_HOUR
            let since           = moment (until.valueOf() - timespan)
            let query           = {"since":since.format("YYYY-MM-DDTHH:mm:ss"), "to":to.format('YYYY-MM-DDTHH:mm:ss')};
            
            try {
                let response    = await this.build_request("get", request_url, query, undefined)
                if (response.data.data!=undefined && isArray(response.data.data)) {
                    _.reverse(response.data.data).map((item:any, idx:number) => {
                        results.push(item)
                    })
                }
            } catch (err : any) {
                //console.error (`Catched an error: ${err.message}`)
            }

            iterations_count++
        }

        return results.slice(0, items_count)
    }

    private async get_datastream_items(path:string, since:moment.Moment, to:moment.Moment|undefined = undefined) {
        if (!to)
            to  = moment()
        
        const request_url   = new URL(path, this.get_appengine_url())
        let query           = {"since":since.format("YYYY-MM-DDTHH:mm:ss"), "to":to.format('YYYY-MM-DDTHH:mm:ss')}
        
        return this.build_request("get", request_url, query, undefined)
    }

    private async get_property(path:string) {
        const request_url   = new URL(path, this.get_appengine_url())
        return this.build_request("get", request_url, undefined, undefined)
    }

    private async update_property(path:string, value:any) {
        const request_url   = new URL(path, this.get_appengine_url())
        console.log (`requurl ${request_url.toString()}`)
        return this.build_request("post", request_url, undefined, value)
    }

    private async publish_datatstream_item(path:string, data:any) {
        const request_url   = new URL(path, this.get_appengine_url())
        return this.build_request("POST", request_url, undefined, data)
    }


    // ================================================================================


    async getSceneSettings ({deviceId}: {deviceId: string}) {
        const {realm, token}  = this.config;
        const interfaceName                 = "ai.clea.examples.SceneSettings";
        const path                          = `v1/${realm}/devices/${deviceId}/interfaces/${this.scene_settings_interface}`;
        const requestUrl                    = new URL(path, this.astarteClient.getAppEngineUrl());
        
        return axios ({
            method  : "get",
            url     : requestUrl.toString(),
            headers : {
                "Authorization" : `Bearer ${token}`,
                "Content-Type"  : "application/json;charset=UTF-8",
            },
            validateStatus : (status) => {return true}
        }).then ((response) => {
            let scene_zones     = response.data.data["scene_zones"]
            let parsed_zones    = []
            for (let i in scene_zones) {
                parsed_zones.push (JSON.parse(scene_zones[i]))
            }

            return parsed_zones
        })
    }



    async getUpdateInterval ({deviceId}: {deviceId: string}) {
        const {realm, token}  = this.config;
        const interfaceName                 = "ai.clea.examples.SceneSettings";
        const path                          = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}`;
        const requestUrl                    = new URL(path, this.astarteClient.getAppEngineUrl());
        
        return axios ({
            method  : "get",
            url     : requestUrl.toString(),
            headers : {
                "Authorization" : `Bearer ${token}`,
                "Content-Type"  : "application/json;charset=UTF-8",
            },
            validateStatus : (status) => {return true}
        }).then ((response) => {
            return response.data.data["update_interval"]
        })
    }



    async getMultipleCameraData ({deviceId, since, to}:MultipleCameraDataParameters) {
        // Retrieving camera data 12 hours for 12 jours
        const PROMISES_MAX_LENGTH               = 50;
        const {realm, token }                   = this.config;
        const path                              = `v1/${realm}/devices/${deviceId}/interfaces/${this.people_counter_interface}/camera`;
        const requestUrl                        = new URL(path, this.astarteClient.getAppEngineUrl());

        let promises                            = [];
        let results                             = [];
        let tmp_start_date                      = new Date(since);
        let tmp_end_date                        = new Date(since);
        tmp_end_date.setHours(tmp_end_date.getHours()+12);

        while (tmp_start_date < to) {
            if (tmp_end_date>to) {
                tmp_end_date    = new Date(to)
            }
            
            const query: Record<string, string> = {};
            query.since                         = tmp_start_date.toISOString();
            query.to                            = tmp_end_date.toISOString();
            requestUrl.search = new URLSearchParams(query).toString();

            promises.push (axios({
                method  : 'get',
                url     : requestUrl.toString(),
                headers : {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json;charset=UTF-8",
                },
                validateStatus : (status) => {return true}
            }))

            // Updating start and end date
            tmp_start_date.setHours(tmp_start_date.getHours()+12)
            tmp_end_date.setHours(tmp_end_date.getHours()+12);

            // Checking if promises has to be awaitied
            if (promises.length > PROMISES_MAX_LENGTH) {
                for (let i in promises) {
                    try {
                        let res = await promises[i]
                        for (let ri in res.data.data) {
                            let item        = res.data.data[ri]
                            results.push ({
                                people          : item.people,
                                people_count    : item.people_count,
                                timestamp       : item.timestamp
                            })
                        }
                    } catch (err) {
                        // Do nothing
                        console.warn (`Catched an error`)
                    }
                }
                promises    = []
            }
        }

        // Awaiting remaining promises
        for (let i in promises) {
            try {
                let res = await promises[i]
                for (let ri in res.data.data) {
                    let item        = res.data.data[ri]
                    results.push ({
                        people          : item.people,
                        people_count    : item.people_count,
                        timestamp       : item.timestamp
                    })
                }
            } catch (err) {
                // Do nothing
                console.warn (`Catched another error`)
            }
        }

        return results;
    }



    async getCameraData({deviceId, sinceAfter, since, to, limit}: CameraDataParameters) {
        const {realm, token } = this.config;
        const path = `v1/${realm}/devices/${deviceId}/interfaces/${this.people_counter_interface}/camera`;
        const requestUrl = new URL(path, this.astarteClient.getAppEngineUrl());
        const query: Record<string, string> = {};
        if (sinceAfter) {
            query.sinceAfter = sinceAfter;
        }
        if (since) {
            query.since = since.toISOString();
        }
        if (to) {
            query.to = to.toISOString();
        }
        if (limit) {
            query.limit = limit.toString();
        }
        requestUrl.search = new URLSearchParams(query).toString();
        return axios({
            method: "get",
            url: requestUrl.toString(),
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json;charset=UTF-8",
            },
            validateStatus : (status) => {return true}
        }).then((response) => {
            return response.data.data;
        });
    }
}

export default AstarteInterface;