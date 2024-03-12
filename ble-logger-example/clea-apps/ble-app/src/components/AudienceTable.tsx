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

import React from "react";
import { FormattedMessage } from "react-intl";
import Table from "react-bootstrap/Table";
import _ from "lodash";

const isValidNumber = (value: unknown): value is number => _.isFinite(value);

type AudienceData = {
  averagePph?: number;
  totalPresence?: number;
  trendPercent?: number;
  trendPph?: number;
};

type Props = {
  data: AudienceData;
};

const AudienceTable = ({ data }: Props) => {
  const { averagePph, totalPresence, trendPercent, trendPph } = data;
  return (
    <Table responsive hover>
      <thead className="border-top">
        <tr>
          <th>
            <FormattedMessage
              id="audience-total-presence"
              defaultMessage="Total Presence"
            />
          </th>
          <th>
            <FormattedMessage
              id="audience-average-pph"
              defaultMessage="Average (Pph)"
            />
          </th>
          <th>
            <FormattedMessage
              id="audience-trend-pph"
              defaultMessage="Trend (Pph)"
            />
          </th>
          <th>
            <FormattedMessage
              id="audience-trend-percent"
              defaultMessage="Trend (%)"
            />
          </th>
        </tr>
      </thead>
      <tbody className="border-top-0">
        <tr>
          <td>
            {isValidNumber(totalPresence) ? totalPresence.toFixed(0) : "-"}
          </td>
          <td>{isValidNumber(averagePph) ? averagePph.toFixed(2) : "-"}</td>
          <td>{isValidNumber(trendPph) ? trendPph.toFixed(2) : "-"}</td>
          <td>{isValidNumber(trendPercent) ? trendPercent.toFixed(2) : "-"}</td>
        </tr>
      </tbody>
    </Table>
  );
};

export type { AudienceData };

export default AudienceTable;
