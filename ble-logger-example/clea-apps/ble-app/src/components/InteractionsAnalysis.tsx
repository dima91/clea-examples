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
import InteractionsChart from "./InteractionsChart";
import InteractionsTable from "./InteractionsTable";
import {
  adjustPresenceCount,
  adjustInteractionsCount,
  BLEStats,
  filterByTimestamp,
  getTimeUnit,
  useBLEStats,
} from "../contexts/BLEStats";

function getChartData(stats: BLEStats, dateRange: [Date, Date]) {
  const timeUnit = getTimeUnit(dateRange);
  const aggregatedStats = filterByTimestamp(stats[timeUnit], dateRange);
  const presence = aggregatedStats.map((d) => ({
    timestamp: d.timestamp,
    value: adjustPresenceCount(timeUnit, d.detectedSmartphones.length),
  }));
  const interactions = aggregatedStats.map((d) => ({
    timestamp: d.timestamp,
    value: adjustInteractionsCount(timeUnit, d.interactions.length),
  }));
  return { presence, interactions };
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
  const interactions = _.flatMap(aggregatedStats, (d) => d.interactions);
  const averageDuration = _.mean(interactions);
  const totalInteractions = adjustInteractionsCount(
    dateRange,
    interactions.length
  );
  const interactionRate = (totalInteractions / totalPresence) * 100;
  return {
    averageDuration,
    interactionRate,
    totalInteractions,
    totalPresence,
  };
}

const InteractionsAnalysis = () => {
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
            id="interaction-analysis-title"
            defaultMessage="Interaction Analysis"
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
        <InteractionsChart data={chartData} xRange={dateRange} />
        <InteractionsTable data={tableData} />
      </Stack>
    </Card>
  );
};

export default InteractionsAnalysis;
