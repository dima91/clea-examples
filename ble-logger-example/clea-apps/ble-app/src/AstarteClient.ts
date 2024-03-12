/*
   Copyright 2022 SECO Mind srl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

import axios from "axios";

type AstarteClientProps = {
  astarteUrl: URL;
  realm: string;
  token: string;
};

type Config = AstarteClientProps & {
  appEngineUrl: URL;
};

type GetInterfaceDataParams = {
  deviceId: string;
  interfaceName: string;
  interfacePath?: string;
  sinceAfter?: string;
  since?: Date;
  to?: Date;
  limit?: number;
};

type GetMinuteStatsParams = {
  deviceId: string;
  sinceAfter?: string;
  since?: Date;
  to?: Date;
  limit?: number;
};
type GetHourStatsParams = GetMinuteStatsParams;
type GetDayStatsParams = GetMinuteStatsParams;

type MacAddress = string;

type RawStats = {
  timestamp: string;
  detectedSmartphones: string[];
  detectedAccessories: string[];
  interactions: number[];
  smartphonesVendors: string;
  accessoriesVendors: string;
};

type AggregatedStats = {
  timestamp: string;
  detectedSmartphones: string[];
  detectedAccessories: string[];
  interactions: number[];
  smartphonesVendors: { [vendorName: string]: MacAddress[] };
  accessoriesVendors: { [vendorName: string]: MacAddress[] };
};
type MinuteStats = AggregatedStats;
type HourStats = AggregatedStats;
type DayStats = AggregatedStats;

function parseJSON<Data = any>(s: string): Data | null {
  try {
    return JSON.parse(s);
  } catch {
    return null;
  }
}

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

  private async getInterfaceData<Data = any>({
    deviceId,
    interfaceName,
    interfacePath = "",
    sinceAfter,
    since,
    to,
    limit,
  }: GetInterfaceDataParams): Promise<Data> {
    const { appEngineUrl, realm, token } = this.config;
    const path = `v1/${realm}/devices/${deviceId}/interfaces/${interfaceName}${interfacePath}`;
    const requestUrl = new URL(path, appEngineUrl);
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
    }).then((response) => response.data.data.statistics);
  }

  async getMinuteStats(params: GetMinuteStatsParams): Promise<MinuteStats[]> {
    return this.getInterfaceData<RawStats[]>({
      ...params,
      interfaceName: "ai.clea.examples.blelogger.MinuteStats",
    }).then((data) =>
      data.map((d) => ({
        timestamp: d.timestamp,
        detectedSmartphones: d.detectedSmartphones || [],
        detectedAccessories: d.detectedAccessories || [],
        interactions: d.interactions || [],
        smartphonesVendors: parseJSON(d.smartphonesVendors) || {},
        accessoriesVendors: parseJSON(d.accessoriesVendors) || {},
      }))
    );
  }

  async getHourStats(params: GetHourStatsParams): Promise<HourStats[]> {
    return this.getInterfaceData<RawStats[]>({
      ...params,
      interfaceName: "ai.clea.examples.blelogger.HourlyStats",
    }).then((data) =>
      data.map((d) => ({
        timestamp: d.timestamp,
        detectedSmartphones: d.detectedSmartphones || [],
        detectedAccessories: d.detectedAccessories || [],
        interactions: d.interactions || [],
        smartphonesVendors: parseJSON(d.smartphonesVendors) || {},
        accessoriesVendors: parseJSON(d.accessoriesVendors) || {},
      }))
    );
  }

  async getDayStats(params: GetDayStatsParams): Promise<DayStats[]> {
    return this.getInterfaceData<RawStats[]>({
      ...params,
      interfaceName: "ai.clea.examples.blelogger.DailyStats",
    }).then((data) =>
      data.map((d) => ({
        timestamp: d.timestamp,
        detectedSmartphones: d.detectedSmartphones || [],
        detectedAccessories: d.detectedAccessories || [],
        interactions: d.interactions || [],
        smartphonesVendors: parseJSON(d.smartphonesVendors) || {},
        accessoriesVendors: parseJSON(d.accessoriesVendors) || {},
      }))
    );
  }
}

export type { MinuteStats, HourStats, DayStats };

export default AstarteClient;
