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
import ReactDOM from "react-dom";
import { FormattedMessage, IntlProvider } from "react-intl";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Nav from "react-bootstrap/Nav";
import Row from "react-bootstrap/Row";
import Stack from "react-bootstrap/Stack";
import Tab from "react-bootstrap/Tab";

import AstarteProvider from "./contexts/Astarte";

import en from "./lang-compiled/en.json";
import it from "./lang-compiled/it.json";

// @ts-ignore
import appStyle from "./style.css";
// @ts-ignore
import datePickerStyle from "react-datepicker/dist/react-datepicker.css";

import Icon from "./components/Icon";
import AudienceAnalysis from "./components/AudienceAnalysis";
import InteractionsAnalysis from "./components/InteractionsAnalysis";
import VendorAnalysis from "./components/VendorAnalysis";

const messages = { en, it };

const App = () => {
  return (
    <div className="p-3 position-relative">
      <Tab.Container id="app-menu" defaultActiveKey="audience">
        <Row>
          <Col sm={3}>
            <Card className="border-0 pe-4">
              <Nav variant="pills" className="flex-column">
                <Nav.Item role="button">
                  <Nav.Link
                    eventKey="audience"
                    className="d-flex align-items-center"
                  >
                    <Icon
                      icon="audience"
                      className="me-2"
                      style={{ height: "1rem" }}
                    />
                    <FormattedMessage
                      id="menu-audience-item"
                      defaultMessage="Audience"
                    />
                  </Nav.Link>
                </Nav.Item>
                <Nav.Item role="button">
                  <Nav.Link
                    eventKey="interactions"
                    className="d-flex align-items-center"
                  >
                    <Icon
                      icon="interaction"
                      className="me-2"
                      style={{ height: "1rem" }}
                    />
                    <FormattedMessage
                      id="menu-interactions-item"
                      defaultMessage="Interactions"
                    />
                  </Nav.Link>
                </Nav.Item>
              </Nav>
            </Card>
          </Col>
          <Col sm={9} className="content-card ps-4">
                <Tab.Content>
                <Tab.Pane eventKey="audience">
                    <Stack gap={3}>
                    <AudienceAnalysis />
                    <VendorAnalysis />
                    </Stack>
                </Tab.Pane>
                <Tab.Pane eventKey="interactions">
                    <InteractionsAnalysis />
                </Tab.Pane>
                </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
    </div>
  );
};

type AppProps = {
  astarteUrl: URL;
  realm: string;
  token: string;
  deviceId: string;
};

type UserPreferences = {
  language: "en" | "it";
};

type Settings = {
  themeUrl: string;
  userPreferences: UserPreferences;
};

const AppLifecycle = {
  mount: (container: ShadowRoot, appProps: AppProps, settings: Settings) => {
    const { themeUrl, userPreferences } = settings;
    const { language } = userPreferences;

    ReactDOM.render(
      <>
        <link href={themeUrl} type="text/css" rel="stylesheet" />
        <style>{appStyle.toString()}</style>
        <style>{datePickerStyle.toString()}</style>
        <IntlProvider
          messages={messages[language]}
          locale={language}
          defaultLocale="en"
        >
          <AstarteProvider {...appProps}>
            <App />
          </AstarteProvider>
        </IntlProvider>
      </>,
      container
    );
  },
  unmount: (container: ShadowRoot) =>
    ReactDOM.unmountComponentAtNode(container),
};

export default AppLifecycle;
