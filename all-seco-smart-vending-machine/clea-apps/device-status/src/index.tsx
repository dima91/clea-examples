import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { IntlProvider, FormattedMessage, useIntl } from "react-intl";
import moment from "moment";

import AstarteInterface from "../../commons/AstarteInterface";

import en from "./lang/en.json";
import it from "./lang/it.json";

// include all style
// @ts-ignore
import appStyle from './css/app.css';
// @ts-ignore
import chartsStyle from "apexcharts/dist/apexcharts.css";

import { MainApp } from "./mainApp";

const messages                          = { en, it };
const { useEffect, useMemo, useState }  = React;

type AppProps = {
    astarteUrl: URL;
    realm: string;
    token: string;
    deviceId: string;
};

type Settings = {
    themeUrl: string;
    userPreferences: UserPreferences;
}

const App = ({ astarteUrl, realm, token, deviceId }: AppProps) => {
    // App config variables
    const [status, set_status]                  = useState<Object | undefined>(undefined)
    const [device_setup, set_setup]             = useState<Object | undefined>(undefined)
    const [introspection, set_introspection]    = useState<Object | undefined>(undefined);
    const [is_ready, set_is_ready]              = useState<Boolean>(false)

    // Setting up astarteClient
    const astarte_interface = useMemo(() => {
        return new AstarteInterface({ astarteUrl, realm, token, deviceId });
    }, [astarteUrl, realm, token]);

    // Retrieving initial information from external sources
    useEffect (() => {
        astarte_interface.get_introspection()
        .then ((data:any) => {
            set_introspection (data)
        })
    }, [astarte_interface])
    useEffect (() => {
        astarte_interface.get_last_device_status(1)
        .then ((data:any) => {
            set_status(data[0])
        })
    }, [astarte_interface])
    useEffect (() => {
        astarte_interface.get_device_setup()
        .then ((data:any) => {
            set_setup(data)
        })
    }, [astarte_interface])

    useEffect(() => {
        set_is_ready(status!=undefined && device_setup!=undefined && introspection!=undefined)
    }, [status, device_setup, introspection])

    return (
        <Fragment>
            <MainApp is_ready={is_ready} astarte={astarte_interface} introspection={introspection} device_status={status} device_setup={device_setup}/>
        </Fragment>
    );
};


type UserPreferences = {
    language: "en" | "it";
};

const AppLifecycle = {
    mount: (
        container: ShadowRoot,
        appProps: AppProps,
        settings: Settings
    ) => {
        const { themeUrl, userPreferences } = settings;
        const { language } = userPreferences;

        ReactDOM.render(
            <>
                <link href={themeUrl} type="text/css" rel="stylesheet" />
                <style>{chartsStyle.toString()}</style>
                <style>{appStyle.toString()}</style>
                <IntlProvider
                    messages={messages[language]}
                    locale={language}
                    defaultLocale="en"
                >
                    <App {...appProps} />
                </IntlProvider>
            </>,
            container
        );
    },
    unmount: (container: ShadowRoot) =>
        ReactDOM.unmountComponentAtNode(container),
};

export default AppLifecycle;
