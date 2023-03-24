
import React from "react";
import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, Spinner, Navbar, Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import _ from 'lodash';

import Commons from "commons/Commons";
import AstarteInterface from "commons/AstarteInterface";
import StatusOverview from "./components/StatusOverview";
import ChartCard from "commons/ChartCard";
import MapCard from "commons/MapCard";
import SelectorsListCard from "commons/SelectorsListCard";



type MainAppProps   = {
    is_ready:Boolean
    astarte:AstarteInterface
    introspection:any
    device_status:any
    device_setup:any
}

type SelectorsDescripts = {
    [key: string]: any;
};

export const MainApp = ({is_ready, astarte, introspection, device_status, device_setup}:MainAppProps) => {
    
    const [current_temperature, set_temperature]    = React.useState<number>(0)
    const [current_consumption, set_consumption]    = React.useState<number>(0)
    const [current_vibration, set_vibration]        = React.useState<number>(0)
    const [current_efficiency, set_efficiency]      = React.useState<number>(0)
    const [current_setup, set_device_setup]         = React.useState<any>({})
    
    const OVERVIEW_K:string         = "OVERVIEW"
    const CHAMBER_TEMP_K:string     = "CHAMBER_TEMP"
    const PWR_CONSUMPTION_K:string  = "PWR_CONSUMPTION"
    const ENGINE_VIBR_K:string      = "ENGINE_VIBR"

    const [selected_descriptor_key, set_descriptor_key] = React.useState<string>(OVERVIEW_K)
    const selectors_descriptors : SelectorsDescripts    = {
        OVERVIEW_K  : {
            descriptor_id   : OVERVIEW_K,
            text            : "Overview",
            on_click        : (item:any) => {set_descriptor_key(OVERVIEW_K); console.log(item)}
        },
        CHAMBER_TEMP_K      : {
            descriptor_id   : CHAMBER_TEMP_K,
            text            : "Chamber Temperature",
            on_click        : (item:any) => {set_descriptor_key(CHAMBER_TEMP_K)},
            data_retriever_cb   : (a:AstarteInterface, s:moment.Moment, t:moment.Moment) => {return a.get_device_status_time_series(s,t)},
            data_filter_cb      : (items:any) => { return _.map(items, (it:any, idx:number) => {
                                                                        return [new Date(it.timestamp), it.chamberTemperature]})}
        },
        PWR_CONSUMPTION_K   : {
            descriptor_id   : PWR_CONSUMPTION_K,
            text            : "Power Consumption",
            on_click        : (item:any) => {set_descriptor_key(PWR_CONSUMPTION_K);}
        },
        ENGINE_VIBR_K       : {
            descriptor_id   : ENGINE_VIBR_K,
            text            : "Engine Vibration",
            on_click        : (item:any) => {set_descriptor_key(ENGINE_VIBR_K)}

        }
    }


    const handle_channel_event = (evt:any) => {
        console.log(`Received a channel event!`)
        console.log(evt)

        if (evt['event']['interface'] == "ai.clea.examples.vendingMachine.DeviceStatus") {
            let val = evt['event']["value"]
            console.log (val)
            set_temperature(val["chamberTemperature"])
            set_vibration(val["engineVibration"])
            set_consumption(val["powerConsumption"])
            set_efficiency(Commons.derive_efficiency(val["cahmberTemperature"], val["powerConsumption"], val["engineVibration"], current_setup))
        }
    }

    const get_selector_text_color   = (id:string) => {
        if (id == selected_descriptor_key)
            return "text-white"
        else
            return ""
    }

    const get_selector_bg_color     = (id:string) => {
        if (id == selected_descriptor_key)
            return "primary-bg"
        else
            return ""
    }


    const on_app_ready  = () => {
        console.log ("App ready!")
        // Assigning initial values
        set_temperature(device_status['chamberTemperature'])
        set_consumption(device_status['powerConsumption'])
        set_vibration(device_status['engineVibration'])
        set_device_setup(device_setup)
        set_efficiency(Commons.derive_efficiency(device_status['chamberTemperature'], device_status['powerConsumption'], device_status['engineVibration'], device_setup))
        
        // Registering to interesting Astarte channels
        astarte.register_incoming_data_trigger (handle_channel_event, astarte.device_setup_interface, "*", "/*")
               .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
        astarte.register_incoming_data_trigger (handle_channel_event, astarte.device_status_interface, "*", "/*")
               .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
    }


    React.useEffect(() => {
        if (is_ready)
            on_app_ready()
    }, [is_ready])


    return (
        <Container fluid>
            {
                !is_ready ?
                    <Row>
                        <div className="m-5 d-flex justify-content-center align-items-center">
                            <Spinner animation="border" role="status" variant="Info">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>
                        </div>
                    </Row>
                :
                    <Col sm={12} md={12}>
                        <Row>
                            <Col sm={3} md={3}>
                                <SelectorsListCard  descriptors={selectors_descriptors}
                                                    selected_selector={{value:selected_descriptor_key, setter:set_descriptor_key}}/>
                                {/* <Card className="shadow rounded">
                                    <Card.Body>
                                        <Nav variant="pills" defaultActiveKey={0}  className="flex-column">
                                            {
                                                _.map(selectors_descriptors, (item:any, key:string, idx:number)=> {
                                                    return (
                                                        <Button key={key} value={item.descriptor_id} onClick={item.on_click} variant=""
                                                                className={`mt-2 text-start ${get_selector_text_color(item.descriptor_id)}
                                                                                        ${get_selector_bg_color(item.descriptor_id)}`}>
                                                            {item.text}
                                                        </Button>
                                                    )
                                                })
                                            }
                                        </Nav>
                                    </Card.Body>
                                </Card> */}
                            </Col>

                            <Col sm={9} md={9}>
                                <Row>
                                    {
                                        selected_descriptor_key == OVERVIEW_K ?
                                            <Row>
                                                <StatusOverview temperature={current_temperature} consumption={current_consumption}
                                                            vibration={current_vibration} efficiency={current_efficiency}
                                                            astarte={astarte} device_setup={current_setup}/>
                                                <Col>
                                                    <MapCard/>
                                                </Col>
                                            </Row>
                                        :
                                            selected_descriptor_key == CHAMBER_TEMP_K ?
                                                <ChartCard astarte={astarte} chart_name={"Chamber Temperature"}
                                                            data_retriever_cb={(a:AstarteInterface, s:moment.Moment, t:moment.Moment) => {
                                                                                    return a.get_device_status_time_series(s,t)}}
                                                            data_filter_cb={(items:any) => {
                                                                                return _.map(items, (it:any, idx:number) => {
                                                                                                return [new Date(it.timestamp), it.chamberTemperature]})}}
                                                />
                                            :
                                                selected_descriptor_key == PWR_CONSUMPTION_K ?
                                                    <ChartCard astarte={astarte} chart_name={"Power Consumption"}
                                                                data_retriever_cb={(a:AstarteInterface, s:moment.Moment, t:moment.Moment) => {
                                                                                        return a.get_device_status_time_series(s,t)}}
                                                                data_filter_cb={(items:any) => {
                                                                                    return _.map(items, (it:any, idx:number) => {
                                                                                                    return [new Date(it.timestamp), it.powerConsumption]})}}/>
                                                :

                                                    <ChartCard astarte={astarte} chart_name={"Engine Vibration"}
                                                                data_retriever_cb={(a:AstarteInterface, s:moment.Moment, t:moment.Moment) => {
                                                                                        return a.get_device_status_time_series(s,t)}}
                                                                data_filter_cb={(items:any) => {
                                                                                    return _.map(items, (it:any, idx:number) => {
                                                                                                    return [new Date(it.timestamp), it.engineVibration]})}}/>
                                    }
                                </Row>
                            </Col>
                        </Row>
                    </Col>
            }
        </Container>
    );
}