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

import React, { forwardRef, useCallback, useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import dayjs from "dayjs";

import Icon from "./Icon";

type PickerButtonProps = {
  onClick?: () => void;
};

const PickerButton = forwardRef<HTMLButtonElement, PickerButtonProps>(
  ({ onClick }, ref) => (
    <button
      type="button"
      className="btn text-muted"
      onClick={onClick}
      ref={ref}
    >
      <Icon icon="calendar" style={{ height: "1rem" }} />
    </button>
  )
);

type DateRangePickerProps = {
  value: [Date, Date];
  disabled?: boolean | undefined;
  onChange: (dates: [Date, Date]) => void;
};

const DateRangePicker = ({
  value,
  disabled,
  onChange,
}: DateRangePickerProps) => {
  const [dateRange, setDateRange] = useState<[Date | null, Date | null]>(value);

  useEffect(() => {
    setDateRange(value);
  }, [value]);

  const handleChange = useCallback(
    (newDateRange: [Date | null, Date | null]) => {
      setDateRange(newDateRange);
      if (newDateRange[0] != null && newDateRange[1] != null) {
        onChange(newDateRange as [Date, Date]);
      }
    },
    [onChange]
  );

  const minDate = dayjs().subtract(1, "year").toDate();
  // Be sure that today is always included in the range
  const maxDate = dayjs().add(1, "day").toDate();

  return (
    <DatePicker
      className="rounded text-muted p-1"
      customInput={<PickerButton />}
      disabled={disabled}
      monthsShown={2}
      onChange={handleChange}
      startDate={dateRange[0]}
      endDate={dateRange[1]}
      maxDate={maxDate}
      minDate={minDate}
      selectsRange
    />
  );
};

export default DateRangePicker;
