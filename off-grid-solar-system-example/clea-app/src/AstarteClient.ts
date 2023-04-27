import axios, { AxiosInstance } from "axios";

type AstarteClientProps = {
    astarteUrl: URL;
    realm: string;
    token: string;
    deviceId: string;
};

type Config = AstarteClientProps & {
    appeEngineURL: URL;
};

type QueryParameters = {
    sinceAfter?: string;
    since?: Date;
    to?: Date;
    limit?: number;
};

class AstarteClient {
    config: Config;
    EXTERNAL_SENSORS_INTERFACE:string   = `ai.clea.examples.offgrid.ExternalSensors`;
    LOAD_STATISTICS_INTERFACE:string    = `ai.clea.examples.offgrid.LoadStats`;
    BATTERY_STATISTICS_INTERFACE:string = `ai.clea.examples.offgrid.BatteryStats`;
    PANEL_STATISTICS_INTERFACE:string   = `ai.clea.examples.offgrid.PanelStats`;


    constructor({astarteUrl, realm, token, deviceId}: AstarteClientProps) {
        this.config = {
            astarteUrl,
            realm,
            token,
            deviceId,
            appeEngineURL: new URL("/", astarteUrl),
        };
    }


    async performQuery (params:QueryParameters, inerfaceName:string, path?:string) {
        const {appeEngineURL,
                realm,
                token,
                deviceId}       = this.config;
        const finalPath         = `appengine/v1/${realm}/devices/${deviceId}/interfaces` +
                                    `/${inerfaceName}${path!==undefined ? "/"+path : ""}`;
        const requestURL        = new URL(finalPath, appeEngineURL);
        const query: Record<string, string> = {};
        if (params.sinceAfter) {
            query.sinceAfter    = params.sinceAfter;
        }
        if (params.since) {
            query.since = params.since.toISOString();
        }
        if (params.to) {
            query.to    = params.to.toISOString();
        }
        if (params.limit) {
            query.limit = params.limit.toString();
        }
        requestURL.search = new URLSearchParams(query).toString();
        
        return axios ({
            method  : "get",
            url     : requestURL.toString(),
            headers : {
                "Authorization" : `Bearer ${token}`,
                "Content-Type"  : "application/json;charset=UTF-8",
            }
        }).then ((response) => {
            return response.data.data
        })
    }


    async formatData(data:any) {
        return data.map((item:any, idx:any, collection:any) => {
            item.current    = item.current.toFixed(2)
            item.voltage    = item.voltage.toFixed(2)
            return item
        })
    }




    async getTemperature (since:Date) {
        return this.performQuery ({since}, this.EXTERNAL_SENSORS_INTERFACE, "temperature");
    }

    async getWindSpeed (since:Date) {
        return this.performQuery ({since}, this.EXTERNAL_SENSORS_INTERFACE, "wind_velocity");
    }
    
    async getReferenceCellCurrent(since: Date) {
        return this.performQuery ({since}, this.EXTERNAL_SENSORS_INTERFACE, "reference_electrical_current");
    }
    
    async getDayPeriod(since:Date) {
        return this.performQuery ({since}, this.EXTERNAL_SENSORS_INTERFACE, "day_period");
    }


    async getSolarPanelData (since:Date, to:Date) {
        return this.formatData(await this.performQuery ({since, to}, this.PANEL_STATISTICS_INTERFACE, ""))
    }


    async getBatteryData (since:Date, to:Date) {
        return this.formatData(await this.performQuery ({since, to}, this.BATTERY_STATISTICS_INTERFACE, ""))
    }


    async getElectricalLoadData (since:Date, to:Date) {
        return this.formatData(await this.performQuery ({since, to}, this.LOAD_STATISTICS_INTERFACE, ""))
    }
}


export default AstarteClient;