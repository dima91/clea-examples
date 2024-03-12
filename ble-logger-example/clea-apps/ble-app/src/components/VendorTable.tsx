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

import React, { HTMLAttributes, useMemo } from "react";
import { FormattedMessage } from "react-intl";
import Table from "react-bootstrap/Table";
import { useIntl } from "react-intl";
import _ from "lodash";

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

type Props = HTMLAttributes<HTMLTableElement> & {
  data: Vendor[];
};

const VendorTable = ({ data, ...props }: Props) => {
  const vendors = useMajorVendors(data);

  return (
    <Table responsive hover {...props}>
      <thead className="border-top">
        <tr>
          <th>
            <FormattedMessage id="vendor-name" defaultMessage="Vendor" />
          </th>
          <th>
            <FormattedMessage
              id="vendor-device-count"
              defaultMessage="Devices"
            />
          </th>
        </tr>
      </thead>
      <tbody className="border-top-0">
        {vendors.map((vendor) => (
          <tr key={vendor.label}>
            <td>{vendor.label}</td>
            <td>{vendor.value}</td>
          </tr>
        ))}
        {vendors.length === 0 && (
          <tr>
            <td colSpan={2}>
              <FormattedMessage
                id="no-vendor-found"
                defaultMessage="No vendor found"
              />
            </td>
          </tr>
        )}
        <tr>
          <td className="fw-bold">
            <FormattedMessage id="vendor-total-count" defaultMessage="Total" />
          </td>
          <td>{_.sumBy(vendors, "value")}</td>
        </tr>
      </tbody>
    </Table>
  );
};

export type { Vendor };

export default VendorTable;
