
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

class AstarteInterface {
    
    private astarteClient : AstarteClient;
    private config : AstarteInterfaceProps
    private room : String | null

    device_status_interface         = "ai.clea.examples.vendingMachine.DeviceStatus"
    device_setup_interface          = "ai.clea.examples.vendingMachine.DeviceSetup"
    refill_event_interface          = "ai.clea.examples.vendingMachine.RefillEvent"
    product_details_interface       = "ai.clea.examples.vendingMachine.ProductDetails"
    advertisement_details_interface = "ai.clea.examples.vendingMachine.AdvertisementDetails"
    promo_details_interface         = "ai.clea.examples.vendingMachine.PromoDetails"
    sale_product_details_interface  = "ai.clea.examples.vendingMachine.SaleProductDetails"
    transaction_interface           = "ai.clea.examples.vendingMachine.Transaction"
    device_location_interface       = "ai.clea.examples.vendingMachine.DeviceLocation"
    customer_detection_interface    = "ai.clea.examples.vendingMachine.CustomerDetection"


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
                console.error (`Catched an error: ${err.message}`)
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


    async get_last_device_status(items_count:number, until:moment.Moment|undefined = undefined) {
        const path  = `${this.build_path(this.device_status_interface)}/status`
        return this.get_last_datastream_items(path, items_count, until)
    }
    
    
    async get_device_status_time_series(since:moment.Moment, to:moment.Moment) {
        const path  = `${this.build_path(this.device_status_interface)}/status`
        return this.get_datastream_items(path, since, to)
    }
    
    
    async get_device_setup() {
        const path          = `${this.build_path(this.device_setup_interface)}`
        return this.get_property(path).then((response) => response.data?.data)
    }


    async get_sales_product_details() {
        const path  = `${this.build_path(this.sale_product_details_interface)}`
        return this.get_property(path).then((response) => response.data?.data)
    }
    
    
    async get_product_details() {
        let path    = `${this.build_path(this.product_details_interface)}`
        return this.get_property(path).then((response) => response.data?.data)
    }


    async get_last_refill_events(count:number|undefined = undefined) {
        const actual_path   = this.build_path(this.refill_event_interface)
        return this.get_datastream_items(actual_path, moment().subtract(1, 'year'), undefined).then((response) => response.data?.data)
    }


    async set_property(path:string, new_value:any) {
        const actual_path   = `${this.build_path(this.device_setup_interface)}/${path}`
        return this.update_property(actual_path, new_value).then((response) => response)
    }

    async make_refill(note:string, refiller_id:string) {
        let data    = {
            'note'          : note,
            'refillerID'    : refiller_id
        }
        let path    = `${this.build_path(this.refill_event_interface)}/refill`
        return this.publish_datatstream_item(path, data)
        .then((response) => console.log(response))
    }
}

export default AstarteInterface;