import axios from "axios";
import moment from "moment";
import ApiHandler from "./apiHandler.js";

import { AirflowData, AirFluxEvent, AirPollutionData, AirVelocityData } from "./types/index";

type AstarteClientProps = {
    astarteUrl: URL;
    realm: string;
    token: string;
};

type Config = AstarteClientProps & {
    appEngineUrl: URL;
};

type AirFluxDataParameters = {
    deviceId: string;
    endpoint?: string;
    sinceAfter?: Date;
    since?: Date;
    to?: Date;
    limit?: number;
    downsamplingTo?: number;
};

type PhoenixSocketParams = {
    device: string,
    interfaceName: string,
    onInComingData: (data: any) => void,
    onOpenConnection: () => void,
    onCloseConnection: () => void,
    onErrorConnection: () => void
}

class AstarteClient {
    config: Config;
    apiHandler:ApiHandler;

    constructor({ astarteUrl, realm, token }: AstarteClientProps) {
        this.config = {
            astarteUrl,
            realm,
            token,
            appEngineUrl: new URL("appengine/", astarteUrl),
        };
        this.apiHandler = new ApiHandler({endpoint:astarteUrl, realm, token})
        this.apiHandler.connectSocket({})
    }

    /*getWSUrl() {
        const astarteChannelUrl = new URL(
            `/appengine/v1/socket`,
            this.config.astarteUrl
        );
        astarteChannelUrl.protocol = "wss:";
        return astarteChannelUrl;
    }

    getConnectionTriggerPayload(device: string): any {
        return {
            name: `connectiontrigger-${device}`,
            device_id: device,
            simple_trigger: {
                type: "device_trigger",
                on: "device_connected",
                device_id: device,
            },
        };
    }

    getDisconnectionTriggerPayload(device: string): any {
        return {
            name: `disconnectiontrigger-${device}`,
            device_id: device,
            simple_trigger: {
                type: "device_trigger",
                on: "device_disconnected",
                device_id: device,
            },
        };
    }

    getValueTriggerPayload(device: string, interfaceName: string, value_match_operator = "*", known_value = 0,): any {
        return {
            name: `valueTrigger-${device}`,
            device_id: device,
            simple_trigger: {
                type: "data_trigger",
                on: "incoming_data",
                interface_name: interfaceName,
                interface_major: 1,
                match_path: "*",
                known_value: known_value,
                value_match_operator: value_match_operator,
            },
        };
    }*/

    async getAirFlowValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo }: AirFluxDataParameters): Promise<AirflowData[]> {
        return this.getAirFluxValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo, endpoint: "flow" });
    }
    async getPollutionValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo }: AirFluxDataParameters): Promise<AirPollutionData[]> {
        return this.getAirFluxValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo, endpoint: "pollution" });
    }
    async getVelocityValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo }: AirFluxDataParameters): Promise<AirVelocityData[]> {
        return this.getAirFluxValues({ deviceId, sinceAfter, since, to, limit, downsamplingTo, endpoint: "velocity" });
    }

    private async getAirFluxValues({
        deviceId,
        endpoint,
        sinceAfter,
        since,
        to,
        limit,
        downsamplingTo,
    }: AirFluxDataParameters): Promise<AirflowData[] | AirPollutionData[] | AirVelocityData[]> {
        const { appEngineUrl, realm, token } = this.config;
        const interfaceName = "ai.clea.examples.AirData";
        const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}/${endpoint}`;
        const requestUrl = new URL(path, appEngineUrl);
        const query: Record<string, string> = {};
        if (sinceAfter) {
            query.since_after = sinceAfter.toISOString();
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
            // console.log("[AirFluxQuery] Got response from Astarte:", response);
            if (response.data.data) {
                return response.data.data.map((datapoint: any) => {
                    return { value: datapoint.value, timestamp: moment.utc(datapoint.timestamp).valueOf() };
                });
            }
            return [];
        });
    }

    async getFluxEventsHistoryValues({
        deviceId,
        endpoint,
        sinceAfter,
        since,
        to,
        limit,
        downsamplingTo,
    }: AirFluxDataParameters): Promise<AirFluxEvent[]> {
        const { appEngineUrl, realm, token } = this.config;
        const interfaceName = "ai.clea.examples.EventsHistory";
        const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}/${endpoint}`;
        const requestUrl = new URL(path, appEngineUrl);
        const query: Record<string, string> = {};
        if (sinceAfter) {
            query.since_after = sinceAfter.toISOString();
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
            // console.log("[EventsHistoryQuery] Got response from Astarte:", response);
            if (response.data.data) {
                return response.data.data.map((datapoint: any) => {
                    return {
                        detection: datapoint.detection,
                        measure: datapoint.measure,
                        noteCode: datapoint.noteCode,
                        timestamp: moment.utc(datapoint.timestamp).valueOf(),
                    };
                });
            }
            return [];
        });
    }


    /*connectSocket(params: PhoenixSocketParams): number {
        const {
            device,
            interfaceName,
            onInComingData,
            onOpenConnection = () => { },
            onCloseConnection = () => { },
            onErrorConnection = () => { },
        } = params;
        const socketUrl = this.getWSUrl();
        const socketParams = {
            params: {
                realm: this.config.realm,
                token: this.config.token,
            },
        };
        const phoenixSocket = new Socket(socketUrl.toString(), socketParams);
        phoenixSocket.onOpen(onOpenConnection);
        phoenixSocket.onError(onErrorConnection);
        phoenixSocket.onClose(onCloseConnection);
        phoenixSocket.onMessage(onInComingData);
        phoenixSocket.connect();

        const room_name = Math.random().toString(36).substring(7);
        const channel = phoenixSocket.channel(
            `rooms:${this.config.realm}:${device}_${room_name}`,
            { token: this.config.token }
        );
        channel.join().receive("ok", (response: any) => {
            channel.push("watch", this.getConnectionTriggerPayload(device));
            channel.push("watch", this.getDisconnectionTriggerPayload(device));
            channel.push(
                "watch",
                this.getValueTriggerPayload(
                    device,
                    interfaceName,
                )
            );
        });
        this.sockets.push(phoenixSocket);
        return this.sockets.indexOf(phoenixSocket)
    }

    disconnectSocket(idx: number) {
        this.sockets[idx].disconnect();
    }*/
}

export default AstarteClient;
