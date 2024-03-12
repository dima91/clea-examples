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

import React, { useMemo } from "react";
import { useIntl } from "react-intl";
import Chart from "react-apexcharts";
import type { ApexOptions } from "apexcharts";

const chartOptions: ApexOptions = {
  chart: {
    animations: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  colors: ["#66CA26", "#E68C00"],
  yaxis: {
    tooltip: {
      enabled: false,
    },
  },
  xaxis: {
    type: "datetime",
    labels: {
      datetimeUTC: false,
    },
    axisBorder: {
      show: false,
    },
  },
  legend: {
    position: "top",
    horizontalAlign: "left",
    offsetX: 10,
  },
  grid: {
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
    padding: {
      top: -10,
    },
  },
  stroke: {
    curve: "smooth",
  },
};

type Props = {
  data: {
    presence: { timestamp: string; value: number }[];
    interactions: { timestamp: string; value: number }[];
  };
  xRange?: [Date, Date];
};

const InteractionsChart = ({
  data: { presence, interactions },
  xRange,
}: Props) => {
  const intl = useIntl();

  const options: ApexOptions = useMemo(() => {
    return {
      ...chartOptions,
      chart: {
        ...chartOptions.chart,
        id: `line${Math.random()}`, // https://github.com/apexcharts/react-apexcharts/issues/146
      },
      xaxis: {
        ...chartOptions.xaxis,
        min: xRange && xRange[0].getTime(),
        max: xRange && xRange[1].getTime(),
      },
      yaxis: {
        ...chartOptions.yaxis,
        labels: {
          formatter: (value?: number) => {
            return value != null ? value.toFixed(0) : "";
          },
        },
      },
    };
  }, [xRange]);

  const series = useMemo(() => {
    return [
      {
        name: intl.formatMessage({
          id: "interactions-chart-presence",
          defaultMessage: "Presence",
        }),
        data: presence.map((a) => [new Date(a.timestamp), a.value]),
        type: "column",
      },
      {
        name: intl.formatMessage({
          id: "interactions-chart-interactions",
          defaultMessage: "Interactions",
        }),
        data: interactions.map((i) => [new Date(i.timestamp), i.value]),
        type: "column",
      },
    ];
  }, [presence, interactions]);

  // @ts-expect-error wrong Apexcharts types
  return <Chart type="line" height={400} options={options} series={series} />;
};

export default InteractionsChart;
