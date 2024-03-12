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

import React, { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import Card from "react-bootstrap/Card";
import Nav from "react-bootstrap/Nav";
import useInterval from "react-use/lib/useInterval";
import dayjs from "dayjs";

import DateRangePicker from "./DateRangePicker";

type ActiveRange = "hour" | "day" | "week" | "month" | "year";

function getDateRange(activeRange: ActiveRange): [Date, Date] {
  switch (activeRange) {
    case "hour":
      return [dayjs().subtract(1, "hour").toDate(), dayjs().toDate()];
    case "day":
      return [dayjs().subtract(1, "day").toDate(), dayjs().toDate()];
    case "week":
      return [dayjs().subtract(1, "week").toDate(), dayjs().toDate()];
    case "month":
      return [dayjs().subtract(1, "month").toDate(), dayjs().toDate()];
    case "year":
      return [dayjs().subtract(1, "year").toDate(), dayjs().toDate()];
  }
}

type MenuButtonProps = {
  active?: boolean;
  children?: React.ReactNode;
  className?: string;
  onClick?: () => void;
};

const MenuButton = ({
  active = false,
  children,
  className = "",
  onClick,
}: MenuButtonProps) => {
  return active ? (
    <button
      type="button"
      className={
        "btn action-button bg-white text-primary border shadow-sm fw-bold " +
        className
      }
      onClick={onClick}
      disabled
    >
      {children}
    </button>
  ) : (
    <button
      type="button"
      className={"btn text-muted " + className}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

type Props = {
  className?: string;
  onChange: ([start, end]: [Date, Date]) => void;
  value: [Date, Date];
};

const DateRangeMenu = ({ className = "", onChange, value }: Props) => {
  const [activeMenuItem, setActiveMenuItem] = useState<ActiveRange | null>(
    "hour"
  );

  const handleClickHour = useCallback(() => {
    setActiveMenuItem("hour");
    onChange(getDateRange("hour"));
  }, [onChange]);

  const handleClickDay = useCallback(() => {
    setActiveMenuItem("day");
    onChange(getDateRange("day"));
  }, [onChange]);

  const handleClickWeek = useCallback(() => {
    setActiveMenuItem("week");
    onChange(getDateRange("week"));
  }, [onChange]);

  const handleClickMonth = useCallback(() => {
    setActiveMenuItem("month");
    onChange(getDateRange("month"));
  }, [onChange]);

  const handleSelectRange = useCallback(
    (dateRange: [Date, Date]) => {
      setActiveMenuItem(null);
      onChange(dateRange);
    },
    [onChange]
  );

  useInterval(() => {
    if (!activeMenuItem) {
      // A custom range is selected, no need to update it
      return;
    }
    // A menu item is selected, keep updating the range to get latest data
    onChange(getDateRange(activeMenuItem));
  }, 10 * 1000);

  return (
    <Card className={"p-2 border-0 bg-light " + className}>
      <Nav
        role="tablist"
        as="ul"
        variant="pills"
        className="nav-tabs d-flex align-items-center justify-content-end border-0"
      >
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton
            active={activeMenuItem === "hour"}
            onClick={handleClickHour}
          >
            <FormattedMessage id="date-range-menu-hour" defaultMessage="Hour" />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton
            active={activeMenuItem === "day"}
            onClick={handleClickDay}
          >
            <FormattedMessage id="date-range-menu-day" defaultMessage="Day" />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton
            active={activeMenuItem === "week"}
            onClick={handleClickWeek}
          >
            <FormattedMessage id="date-range-menu-week" defaultMessage="Week" />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton
            active={activeMenuItem === "month"}
            onClick={handleClickMonth}
          >
            <FormattedMessage
              id="date-range-menu-month"
              defaultMessage="Month"
            />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <div style={{ position: "relative", display: "flex" }}>
            <DateRangePicker value={value} onChange={handleSelectRange} />
          </div>
        </Nav.Item>
      </Nav>
    </Card>
  );
};

export default DateRangeMenu;
