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

import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";
import Card from "react-bootstrap/Card";
import Nav from "react-bootstrap/Nav";

type DeviceType = "smartphones" | "accessories" | "all";

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
        " rounded bg-primary text-white fw-bold p-2  " +
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
  onChange: (item: DeviceType) => void;
  value: DeviceType;
};

const DeviceTypeMenu = ({ className = "", onChange, value }: Props) => {
  const handleClickSmartphones = useCallback(() => {
    onChange("smartphones");
  }, [onChange]);

  const handleClickAccessories = useCallback(() => {
    onChange("accessories");
  }, [onChange]);

  const handleClickAll = useCallback(() => {
    onChange("all");
  }, [onChange]);

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
            active={value === "smartphones"}
            onClick={handleClickSmartphones}
          >
            <FormattedMessage
              id="device-type-menu-smartphones"
              defaultMessage="Smartphones"
            />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton
            active={value === "accessories"}
            onClick={handleClickAccessories}
          >
            <FormattedMessage
              id="device-type-menu-accessories"
              defaultMessage="Accessories"
            />
          </MenuButton>
        </Nav.Item>
        <Nav.Item as="li" role="none presentation" className="me-2">
          <MenuButton active={value === "all"} onClick={handleClickAll}>
            <FormattedMessage id="device-type-menu-all" defaultMessage="All" />
          </MenuButton>
        </Nav.Item>
      </Nav>
    </Card>
  );
};

export type { DeviceType };

export default DeviceTypeMenu;
