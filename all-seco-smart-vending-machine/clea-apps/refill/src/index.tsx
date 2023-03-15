
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


type AppProps   = {
    astarteUrl  : URL;
    realm       : string;
    token       : string;
    deviceId    : string;
}

type UserPreferences = {
    language: "en" | "it";
};

type Settings   = {
    themeUrl: string;
    userPreferences: UserPreferences;
}


const messages                          = { en, it };


const App : React.FC<AppProps>  = ({astarteUrl, realm, token, deviceId}:AppProps) => {

    const LAST_REFILL_EVENTS_COUNT                  = 40

    const [is_ready, set_is_ready]                  = React.useState(false)
    const [introspection, set_introspection]        = React.useState<any>(undefined)
    
    
    // Setting up astarteClient
    const astarte_interface = React.useMemo(() => {
        return new AstarteInterface({astarteUrl, realm, token, deviceId});
    }, [astarteUrl, realm, token, deviceId]);

    // Obtaining initial values
    React.useEffect(() => {
        astarte_interface.get_introspection()
        .then((data) => {
            set_introspection(data)
        })
    })

    React.useEffect(() => {
        if (introspection)
            set_is_ready(true)
    }, [astarte_interface, introspection])


    return (
        <Fragment>
            <MainApp is_ready={is_ready} astarte={astarte_interface} introspection={introspection}/>
        </Fragment>
    );
}


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