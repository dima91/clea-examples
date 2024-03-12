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

import { useCallback, useEffect, useMemo, useState } from "react";
import dayjs from "dayjs";

import { MinuteStats, HourStats, DayStats } from "../AstarteClient";
import { useAstarte } from "./Astarte";
import _ from "lodash";

type BLEStats = {
  isLoading: boolean;
  minute: MinuteStats[];
  hour: HourStats[];
  day: DayStats[];
};

function useBLEStats(dateRange: [Date, Date]): BLEStats {
  const [isLoadingMinuteStats, setIsLoadingMinuteStats] = useState(false);
  const [isLoadingHourStats, setIsLoadingHourStats] = useState(false);
  const [isLoadingDayStats, setIsLoadingDayStats] = useState(false);
  const [minuteStats, setMinuteStats] = useState<MinuteStats[]>([]);
  const [hourStats, setHourStats] = useState<HourStats[]>([]);
  const [dayStats, setDayStats] = useState<DayStats[]>([]);
  const { astarteClient, deviceId } = useAstarte();

  const getMinuteStats = useCallback(() => {
    const to = dateRange[1];
    const since = dayjs(to).subtract(2, "day").toDate(); // last 2 days
    if (getTimeUnit(dateRange) !== "minute") {
      // With this date range, minute data will not be needed
      return;
    }
    setIsLoadingMinuteStats(true);
    astarteClient
      .getMinuteStats({ deviceId, since, to })
      .then(setMinuteStats)
      .catch(() => setMinuteStats([]))
      .finally(() => setIsLoadingMinuteStats(false));
  }, [astarteClient, deviceId, dateRange]);

  const getHourStats = useCallback(() => {
    const to = dateRange[1];
    const since = dayjs(to).subtract(1, "year").toDate(); // last year
    if (getTimeUnit(dateRange) !== "hour") {
      // With this date range, hour data will not be needed
      return;
    }
    setIsLoadingHourStats(true);
    astarteClient
      .getHourStats({ deviceId, since, to })
      .then(setHourStats)
      .catch(() => setHourStats([]))
      .finally(() => setIsLoadingHourStats(false));
  }, [astarteClient, deviceId, dateRange]);

  const getDayStats = useCallback(() => {
    const to = dateRange[1];
    const since = dayjs(to).subtract(10, "year").toDate(); // last 10 years
    if (getTimeUnit(dateRange) !== "day") {
      // With this date range, day data will not be needed
      return;
    }
    setIsLoadingDayStats(true);
    astarteClient
      .getDayStats({ deviceId, since, to })
      .then(setDayStats)
      .catch(() => setDayStats([]))
      .finally(() => setIsLoadingDayStats(false));
  }, [astarteClient, deviceId, dateRange]);

  useEffect(getMinuteStats, [getMinuteStats]);
  useEffect(getHourStats, [getHourStats]);
  useEffect(getDayStats, [getDayStats]);

  const isLoading =
    isLoadingMinuteStats || isLoadingHourStats || isLoadingDayStats;

  const stats = useMemo(
    () => ({ isLoading, minute: minuteStats, hour: hourStats, day: dayStats }),
    [isLoading, minuteStats, hourStats, dayStats]
  );

  return stats;
}

type TimeUnit = "minute" | "hour" | "day";

// Hash the timestamp to partion data into buckets of similar data.
// Data grouped together are comparable and can be used to compute a trend.
function getRelevantTimestampPart(timeUnit: TimeUnit, timestamp: string) {
  if (timeUnit === "minute") {
    // Compare similar data using the hour of the day
    return timestamp.slice(11, 13);
  }
  if (timeUnit === "hour") {
    // Compare similar data using the hour of the day
    return timestamp.slice(11, 13);
  }
  // Compare similar data using the day of the month
  return timestamp.slice(8, 10); // TODO: day of the week is probably better
}

function getTimeUnit(dateRange: [Date, Date]): TimeUnit {
  const diffHours = dayjs(dateRange[1]).diff(dateRange[0], "hour", true);
  const diffDays = dayjs(dateRange[1]).diff(dateRange[0], "day", true);
  if (diffHours <= 2) {
    // The time range is less than 2 hours, compute data by minutes
    return "minute";
  }
  if (diffDays <= 3) {
    // The time range is less than 3 days, compute data by hours
    return "hour";
  }
  // The time range is more than 3 days, compute data by days
  return "day";
}

function adjustPresenceCount(
  dateRange: [Date, Date] | TimeUnit,
  count: number
) {
  // Account for random MAC addresses changing every 15 minutes, 4 times per hour
  let generatedMACs = 1;
  switch (dateRange) {
    case "minute":
      break;
    case "hour":
      generatedMACs = 4;
      break;
    case "day":
      generatedMACs = 4 * 24;
      break;
    default: {
      const diffHours = dayjs(dateRange[1]).diff(dateRange[0], "hour", true);
      generatedMACs = diffHours * 4;
    }
  }
  return Math.round(count / generatedMACs);
}

function adjustInteractionsCount(
  dateRange: [Date, Date] | TimeUnit,
  count: number
) {
  // TODO: account for devices that change the MAC address every 15 minutes
  let generatedInteractions = 1;
  switch (dateRange) {
    case "minute":
      // Each address generates 3 interactions per minute.
      generatedInteractions = 3;
      break;
    case "hour":
      generatedInteractions = 1; // TODO
      break;
    case "day":
      generatedInteractions = 1; // TODO
      break;
    default: {
      const diffHours = dayjs(dateRange[1]).diff(dateRange[0], "hour", true);
      generatedInteractions = diffHours * 1; // TODO
    }
  }
  return Math.round(count / generatedInteractions);
}

function filterByTimestamp<Data extends { timestamp: string }>(
  data: Data[],
  dateRange: [Date, Date]
): Data[] {
  return data.filter((d) => {
    const date = new Date(d.timestamp);
    return date >= dateRange[0] && date <= dateRange[1];
  });
}

export {
  adjustInteractionsCount,
  filterByTimestamp,
  adjustPresenceCount,
  getRelevantTimestampPart,
  getTimeUnit,
  useBLEStats,
};

export type { BLEStats };
