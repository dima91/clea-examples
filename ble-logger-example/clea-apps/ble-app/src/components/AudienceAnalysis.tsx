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

import React, { useMemo, useState } from "react";
import { FormattedMessage } from "react-intl";
import Card from "react-bootstrap/Card";
import Spinner from "react-bootstrap/Spinner";
import Stack from "react-bootstrap/Stack";
import dayjs from "dayjs";
import _ from "lodash";

import DateRangeDisplay from "./DateRangeDisplay";
import DateRangeMenu from "./DateRangeMenu";
import AudienceChart from "./AudienceChart";
import AudienceTable from "./AudienceTable";
import {
  adjustPresenceCount,
  BLEStats,
  filterByTimestamp,
  getRelevantTimestampPart,
  getTimeUnit,
  useBLEStats,
} from "../contexts/BLEStats";

function getChartData(stats: BLEStats, dateRange: [Date, Date]) {
  const timeUnit = getTimeUnit(dateRange);
  const aggregatedStats = stats[timeUnit];
  const presence = aggregatedStats.map((d) => ({
    timestamp: d.timestamp,
    value: adjustPresenceCount(timeUnit, d.detectedSmartphones.length),
  }));
  const trend = presence.map((d) => {
    const relevantTimestampPart = getRelevantTimestampPart(
      timeUnit,
      d.timestamp
    );
    const relevantPresence = presence.filter(
      (p) =>
        getRelevantTimestampPart(timeUnit, p.timestamp) ===
        relevantTimestampPart
    );
    return {
      timestamp: d.timestamp,
      value: _.meanBy(relevantPresence, "value"),
    };
  });
  return {
    presence: filterByTimestamp(presence, dateRange),
    trend: filterByTimestamp(trend, dateRange),
  };
}

function getTableData(stats: BLEStats, dateRange: [Date, Date]) {
  const timeUnit = getTimeUnit(dateRange);
  const aggregatedStats = filterByTimestamp(stats[timeUnit], dateRange);
  const detectedSmartphones = _.uniq(
    _.flatMap(aggregatedStats, "detectedSmartphones")
  );
  const totalPresence = adjustPresenceCount(
    dateRange,
    detectedSmartphones.length
  );
  let pph = stats.hour.map((d) => ({
    timestamp: d.timestamp,
    value: adjustPresenceCount("hour", d.detectedSmartphones.length),
  }));
  if (stats.hour.length === 0) {
    // Could not compute PPH from hours data, use minutes data instead
    const detectedSmartphonesByHour: { [hour: string]: string[] } = {};
    for (const d of stats.minute) {
      const hour = d.timestamp.slice(0, 13);
      if (!detectedSmartphonesByHour[hour]) {
        detectedSmartphonesByHour[hour] = [];
      }
      detectedSmartphonesByHour[hour] = _.uniq(
        detectedSmartphonesByHour[hour].concat(d.detectedSmartphones)
      );
    }
    pph = Object.entries(detectedSmartphonesByHour).map(
      ([hour, detectedSmartphones]) => ({
        timestamp: hour + ":59:59.000Z",
        value: adjustPresenceCount("hour", detectedSmartphones.length),
      })
    );
  }
  const averagePph = _.meanBy(filterByTimestamp(pph, dateRange), "value");
  const pphAverageByHour = _.mapValues(
    _.groupBy(pph, (d) => getRelevantTimestampPart(timeUnit, d.timestamp)),
    (ds) => _.meanBy(ds, "value")
  );
  const trendPph = _.mean(Object.values(pphAverageByHour));
  const trendPercent = (trendPph / totalPresence) * 100;
  return {
    totalPresence,
    averagePph,
    trendPph,
    trendPercent,
  };
}

const AudienceAnalysis = () => {
  const [dateRange, setDateRange] = useState<[Date, Date]>([
    dayjs().subtract(1, "hour").toDate(),
    dayjs().toDate(),
  ]);
  const stats = useBLEStats(dateRange);
  const chartData = useMemo(
    () => getChartData(stats, dateRange),
    [stats, dateRange]
  );
  const tableData = useMemo(
    () => getTableData(stats, dateRange),
    [stats, dateRange]
  );

  return (
    <Card className="shadow border-0 p-3">
      <Stack gap={2}>
        <h6 className="text-primary d-flex justify-content-between align-items-center">
          <FormattedMessage
            id="audience-analysis-title"
            defaultMessage="Audience Analysis"
          />
          {stats.isLoading && (
            <Spinner animation="border" role="status" size="sm" />
          )}
        </h6>
        <div className="d-flex justify-content-end align-items-center">
          <DateRangeMenu onChange={setDateRange} value={dateRange} />
        </div>
        <DateRangeDisplay
          value={dateRange}
          className="ms-auto text-muted p-2"
        />
        <AudienceChart data={chartData} xRange={dateRange} />
        <AudienceTable data={tableData} />
      </Stack>
    </Card>
  );
};

export default AudienceAnalysis;
