import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { IntlProvider, FormattedMessage, useIntl } from "react-intl";

import AstarteInterface from "./AstarteInterface";

import en from "./lang/en.json";
import it from "./lang/it.json";

// include all style
// @ts-ignore
import appStyle from './css/app.css';
// @ts-ignore
import chartsStyle from "../node_modules/apexcharts/dist/apexcharts.css";

import { MainApp } from "./MainApp";

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
    const [introspection, setIntrospection]     = useState<Object | null>(null);
    const [isReady, setIsReady]                 = useState<Boolean>(false)
    const [roomsList, setRoomsList]             = useState<Number[] | null> (null);

    // Setting up astarteClient
    const astarteInterface = useMemo(() => {
        return new AstarteInterface({ astarteUrl, realm, token, deviceId });
    }, [astarteUrl, realm, token]);

    // Retrieving initial information from external sources
    useEffect (() => {
        astarteInterface.getIntrospection()
        .then ((data:any) => {
            setIntrospection (data)
        })
    }, [astarteInterface])
    useEffect (() => {
        astarteInterface.getRoomsList()
        .then ((data:any) => {
            setRoomsList (data["roomsIds"])
        })
    }, [astarteInterface])


    useEffect(() => {
        if (introspection!=null && roomsList!=null) {
            setIsReady(true)
        }
    }, [introspection, roomsList])

    return (
        <Fragment>
            <MainApp astarteInterface={astarteInterface} roomsList={roomsList} introspection={introspection} isReady={isReady}/>
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
