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

type InteractionsData = {
  averageDuration?: number;
  interactionRate?: number;
  totalInteractions?: number;
  totalPresence?: number;
};

type Props = {
  data: InteractionsData;
};

const InteractionsTable = ({ data }: Props) => {
  const { averageDuration, interactionRate, totalInteractions, totalPresence } =
    data;
  return (
    <Table responsive hover>
      <thead className="border-top">
        <tr>
          <th>
            <FormattedMessage
              id="interactions-total-presence"
              defaultMessage="Total Presence"
            />
          </th>
          <th>
            <FormattedMessage
              id="interactions-total-interactions"
              defaultMessage="Total Interactions"
            />
          </th>
          <th>
            <FormattedMessage
              id="interactions-interaction-rate"
              defaultMessage="Interaction Rate (%)"
            />
          </th>
          <th>
            <FormattedMessage
              id="interactions-average-duration"
              defaultMessage="Average Duration (s)"
            />
          </th>
        </tr>
      </thead>
      <tbody className="border-top-0">
        <tr>
          <td>
            {isValidNumber(totalPresence) ? totalPresence.toFixed(0) : "-"}
          </td>
          <td>
            {isValidNumber(totalInteractions)
              ? totalInteractions.toFixed(0)
              : "-"}
          </td>
          <td>
            {isValidNumber(interactionRate) ? interactionRate.toFixed(2) : "-"}
          </td>
          <td>
            {isValidNumber(averageDuration) ? averageDuration.toFixed(1) : "-"}
          </td>
        </tr>
      </tbody>
    </Table>
  );
};

export type { InteractionsData };

export default InteractionsTable;
