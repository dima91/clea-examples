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
import { FormattedDate } from "react-intl";

type Props = {
  className?: string;
  value: [Date, Date];
};

const DateRangeDisplay = ({ className, value }: Props) => {
  return (
    <div className={className}>
      <FormattedDate value={value[0]} />
      <span> - </span>
      <FormattedDate value={value[1]} />
    </div>
  );
};

export default DateRangeDisplay;
