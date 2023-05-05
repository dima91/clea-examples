import axios from "axios";
import moment from "moment"

import { TransactionData, BleData, DeviceEntry, RejectedTransactionData } from "./types/index"

type AstarteClientProps = {
  astarteUrl: URL;
  realm: string;
  token: string;
};

type Config = AstarteClientProps & {
  appEngineUrl: URL;
};


type GetTransactionValuesParams = {
  deviceId: string;
  sinceAfter?: Date;
  since?: Date;
  to?: Date;
  limit?: number;
  downsamplingTo?: number;
};


type GetBleDataValuesParams = {
    deviceId: string;
    sinceAfter?: Date;
    since?: Date;
    to?: Date;
    limit?: number;
    downsamplingTo?: number;
};

class AstarteClient {
  config: Config;

  constructor({ astarteUrl, realm, token }: AstarteClientProps) {
    this.config = {
      astarteUrl,
      realm,
      token,
      appEngineUrl: new URL("appengine/", astarteUrl),
    };
  }

  async getTransactionData({ deviceId, sinceAfter, since, to, limit, downsamplingTo }: GetTransactionValuesParams) : Promise<TransactionData[]> {
    const { appEngineUrl, realm, token } = this.config;
    const interfaceName = "ai.clea.examples.face.emotion.detection.Transaction";
    const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}/transaction`;
    const requestUrl = new URL(path, appEngineUrl);
    const query: Record<string, string> = {};
    if (sinceAfter) {
      query.sinceAfter = sinceAfter.toISOString();
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
    if (downsamplingTo) {
      if (downsamplingTo > 2) {
        query.downsample_to = downsamplingTo.toString();
      } else {
        console.warn("[AstarteClient] downsamplingTo must be > 2");
      }
    }
    requestUrl.search = new URLSearchParams(query).toString();
    return axios({
      method: "get",
      url: requestUrl.toString(),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=UTF-8",
      },
    }).then((response) => {
      // console.log("Got response from Astarte:", response);
      if (response.data.data && Array.isArray(response.data.data)) {
        response.data.data.forEach( (datapoint: any) => {
          datapoint.timestamp = moment.utc(datapoint.timestamp).valueOf();
        });
        return response.data.data
      }
      else {
        console.error (`[TRANS] Cannot parse response payload: ${response.data}`)
      }
      return [];
    }).catch ((err) => {
        console.error (`[TRANS] Catched this error:\n${err}`)
        return []
    });
  }


  async getRejectedTransactions ({ deviceId, sinceAfter, since, to, limit, downsamplingTo }: GetTransactionValuesParams) : Promise<RejectedTransactionData[]> {
    const { appEngineUrl, realm, token } = this.config;
    const interfaceName = "ai.clea.examples.face.emotion.detection.RejectedTransaction";
    const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}/transaction`;
    const requestUrl = new URL(path, appEngineUrl);
    const query: Record<string, string> = {};
    if (sinceAfter) {
      query.sinceAfter = sinceAfter.toISOString();
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
    if (downsamplingTo) {
      if (downsamplingTo > 2) {
        query.downsample_to = downsamplingTo.toString();
      } else {
        console.warn("[AstarteClient] downsamplingTo must be > 2");
      }
    }
    requestUrl.search = new URLSearchParams(query).toString();
    return axios({
      method: "get",
      url: requestUrl.toString(),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=UTF-8",
      },
    }).then((response) => {
      // console.log("Got response from Astarte:", response);
      if (response.data.data && Array.isArray(response.data.data)) {
        response.data.data.forEach( (datapoint: any) => {
          datapoint.timestamp = moment.utc(datapoint.timestamp).valueOf();
        });
        return response.data.data
      }
      else {
        console.error (`[TRANS] Cannot parse response payload: ${response.data}`)
      }
      return [];
    }).catch ((err) => {
        console.error (`[TRANS] Catched this error:\n${err}`)
        return []
    });
  }


  async getPaginatedBleData({deviceId, since, to, limit, downsamplingTo} : GetBleDataValuesParams) : Promise<DeviceEntry[]> {

    console.log ("Since:" , since, "\nTo:", to)
      
    if (!since) {
        throw "'since' paramenter not defined"
    }
    if (!to) {
        throw "'to' paramenter not defined"
    }
        
    const MS_PER_TWO_HOURS                      = 2*60*60*1000
    let tmp_results:Promise<DeviceEntry[]>[]    = []
    let tmp_start_date                          = new Date(since)
    let tmp_final_date                          = new Date(since.valueOf()+MS_PER_TWO_HOURS)

    while (tmp_final_date<to){
        tmp_results.push(this.getBleData({deviceId:deviceId, since:tmp_start_date, to:tmp_final_date, limit:limit, downsamplingTo:downsamplingTo}))
        tmp_start_date  = new Date(tmp_final_date.valueOf()+1)
        tmp_final_date  = new Date(tmp_final_date.valueOf()+MS_PER_TWO_HOURS)
    }
    tmp_results.push(this.getBleData({deviceId:deviceId, since:tmp_start_date, to:tmp_final_date, limit:limit, downsamplingTo:downsamplingTo}))

    let results:DeviceEntry[]   = []

    for (let r in tmp_results) {
        let res = await tmp_results[r]
        results = results.concat(res)
    }

    return results
}


  async getBleData ({deviceId, sinceAfter, since, to, limit, downsamplingTo} : GetBleDataValuesParams) : Promise<DeviceEntry[]> {
    const { appEngineUrl, realm, token } = this.config;
    const interfaceName = "ai.clea.examples.BLEDevices";
    const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}/`;
    const requestUrl = new URL(path, appEngineUrl);
    const query: Record<string, string> = {};
    
    if (sinceAfter) {
      query.sinceAfter = sinceAfter.toISOString();
    }
    if (since) {
        // console.log (`Querying for ble from ${since}`)
        query.since = since.toISOString();
    }
    if (to) {
        // console.log (`Querying for ble to ${to}`)
        query.to = to.toISOString();
    }
    if (limit) {
      query.limit = limit.toString();
    }
    if (downsamplingTo) {
      if (downsamplingTo > 2) {
        query.downsample_to = downsamplingTo.toString();
      } else {
        console.warn("[AstarteClient] downsamplingTo must be > 2");
      }
    }
    requestUrl.search = new URLSearchParams(query).toString();
    //console.log (`URL --> ${requestUrl.search}`)

    return axios({
      method: "get",
      url: requestUrl.toString(),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=UTF-8",
      },
    }).then((response) => {
      // console.log("Got BLE response from Astarte:", response);
      let result : any[] = [];
      
      if (response.status=200 && response.data.data && Array.isArray(response.data.data)) {
        response.data.data.forEach ((item:any) => {
            if (Array.isArray(item.devices) && Array.isArray(item.presence_time)) {
                if (item.devices.length != item.presence_time.length) {
                    console.error ("Lengths differs!")
                }
                else {
                    let timestamp   = new Date(item.timestamp)
                    for (let i=0; i<item.devices.length; i++) {
                        result.push({mac:item.devices[i], presence_time:item.presence_time[i], timestamp:Number(timestamp)})
                    }
                }
            }
            else if (item.devices == null && item.presence_time == null) {
                result.push ({mac:undefined, presence_time:undefined, timestamp:Number(new Date(item.timestamp))})
            }
        })
      }
      else {
        //console.error (`[BLE] Cannot parse response payload: `, response)
      }
      result.sort ((a:DeviceEntry, b:DeviceEntry) => a.timestamp-b.timestamp)
      
      return result;
    }).catch ((err) => {
        console.error (`[BLE] Catched this error:\n${err}`)
        return []
    });
  }
}

export default AstarteClient;
