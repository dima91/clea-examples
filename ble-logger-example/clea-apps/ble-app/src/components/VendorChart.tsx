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
import Chart from "react-apexcharts";
import type { ApexOptions } from "apexcharts";
import { useIntl } from "react-intl";
import _ from "lodash";

const chartOptions: ApexOptions = {
  chart: {
    animations: {
      enabled: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  legend: {
    position: "bottom",
  },
};

type Vendor = { label: string; value: number };

function useMajorVendors(vendors: Vendor[]) {
  const intl = useIntl();
  const maxVendors = 10;

  if (vendors.length <= maxVendors) {
    return vendors;
  }

  return useMemo(() => {
    const majorVendors = vendors.slice(0, maxVendors - 1);
    const minorVendors = vendors.slice(maxVendors - 1);
    majorVendors.push({
      label: intl.formatMessage({
        id: "vendor-others",
        defaultMessage: "Others",
      }),
      value: _.sumBy(minorVendors, "value"),
    });
    return majorVendors;
  }, [vendors, intl]);
}

type Props = {
  data: Vendor[];
  xRange?: [Date, Date];
};

const VendorChart = ({ data, xRange }: Props) => {
  const vendors = useMajorVendors(data);

  const options: ApexOptions = useMemo(() => {
    return {
      ...chartOptions,
      chart: {
        ...chartOptions.chart,
        id: `line${Math.random()}`, // https://github.com/apexcharts/react-apexcharts/issues/146
      },
      labels: vendors.map((v) => v.label),
    };
  }, [xRange, vendors]);

  const series = useMemo(() => vendors.map((v) => v.value), [vendors]);

  return <Chart type="donut" height={400} options={options} series={series} />;
};

export type { Vendor };

export default VendorChart;
