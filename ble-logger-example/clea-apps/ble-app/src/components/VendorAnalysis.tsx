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
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Spinner from "react-bootstrap/Spinner";
import Stack from "react-bootstrap/Stack";
import dayjs from "dayjs";
import _ from "lodash";

import DateRangeDisplay from "./DateRangeDisplay";
import DateRangeMenu from "./DateRangeMenu";
import DeviceTypeMenu, { DeviceType } from "./DeviceTypeMenu";
import VendorChart from "./VendorChart";
import VendorTable from "./VendorTable";
import {
  BLEStats,
  filterByTimestamp,
  getTimeUnit,
  useBLEStats,
} from "../contexts/BLEStats";

function getVendorsData(stats: BLEStats, dateRange: [Date, Date]) {
  const timeUnit = getTimeUnit(dateRange);
  const aggregatedStats = filterByTimestamp(stats[timeUnit], dateRange);
  const smartphonesVendors: { [vendor: string]: string[] } = {};
  const accessoriesVendors: { [vendor: string]: string[] } = {};
  const allVendors: { [vendor: string]: string[] } = {};
  for (const d of aggregatedStats) {
    for (const [vendor, macAddresses] of Object.entries(d.smartphonesVendors)) {
      allVendors[vendor] = allVendors[vendor] || [];
      smartphonesVendors[vendor] = smartphonesVendors[vendor] || [];
      smartphonesVendors[vendor] = _.uniq([
        ...smartphonesVendors[vendor],
        ...macAddresses,
      ]);
      allVendors[vendor] = _.uniq([...allVendors[vendor], ...macAddresses]);
    }
    for (const [vendor, macAddresses] of Object.entries(d.accessoriesVendors)) {
      allVendors[vendor] = allVendors[vendor] || [];
      accessoriesVendors[vendor] = accessoriesVendors[vendor] || [];
      accessoriesVendors[vendor] = _.uniq([
        ...accessoriesVendors[vendor],
        ...macAddresses,
      ]);
      allVendors[vendor] = _.uniq([...allVendors[vendor], ...macAddresses]);
    }
  }
  const all = Object.entries(allVendors).map(([vendor, macAddresses]) => ({
    label: vendor,
    value: macAddresses.length,
  }));
  const smartphones = Object.entries(smartphonesVendors).map(
    ([vendor, macAddresses]) => ({
      label: vendor,
      value: macAddresses.length,
    })
  );
  const accessories = Object.entries(accessoriesVendors).map(
    ([vendor, macAddresses]) => ({
      label: vendor,
      value: macAddresses.length,
    })
  );

  return {
    all: _.reverse(_.sortBy(all, "value")),
    smartphones: _.reverse(_.sortBy(smartphones, "value")),
    accessories: _.reverse(_.sortBy(accessories, "value")),
  };
}

const VendorAnalysis = () => {
  const [deviceType, setDeviceType] = useState<DeviceType>("smartphones");
  const [dateRange, setDateRange] = useState<[Date, Date]>([
    dayjs().subtract(1, "hour").toDate(),
    dayjs().toDate(),
  ]);
  const stats = useBLEStats(dateRange);
  const vendors = useMemo(
    () => getVendorsData(stats, dateRange),
    [stats, dateRange]
  );

  const filteredVendors =
    deviceType === "smartphones"
      ? vendors.smartphones
      : deviceType === "accessories"
      ? vendors.accessories
      : vendors.all;

  return (
    <Card className="border-1 p-3">
      <Stack gap={2}>
        <h6 className="text-primary d-flex justify-content-between align-items-center">
          <FormattedMessage
            id="vendor-analysis-title"
            defaultMessage="Vendor Analysis"
          />
          {stats.isLoading && (
            <Spinner animation="border" role="status" size="sm" />
          )}
        </h6>
        <div className="d-flex justify-content-between align-items-center">
          <DeviceTypeMenu onChange={setDeviceType} value={deviceType} />
          <DateRangeMenu onChange={setDateRange} value={dateRange} />
        </div>
        <DateRangeDisplay
          value={dateRange}
          className="ms-auto text-muted p-2"
        />
        <Container fluid>
          <Row>
            {filteredVendors.length > 0 && (
              <Col xs={12} lg={6}>
                <VendorChart data={filteredVendors} xRange={dateRange} />
              </Col>
            )}
            <Col xs={12} lg={filteredVendors.length > 0 ? 6 : 12}>
              <VendorTable data={filteredVendors} className="mt-3" />
            </Col>
          </Row>
        </Container>
      </Stack>
    </Card>
  );
};

export default VendorAnalysis;
