
import "core-js/stable"
import "regenerator-runtime/runtime"
import React, { Fragment } from "react";
import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, Spinner, Navbar, Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import Chart from "react-apexcharts";
import DatePicker from "react-datepicker";
import DatePickerStyle from "react-datepicker";

import AstarteInterface from "../../commons/AstarteInterface";
import { derive_efficiency } from "../../commons/utils";
import StatusOverview from "./components/status_overview";
import DetailedView from "./components/property_detailed_view";
import _ from 'lodash';



type MainAppProps   = {
    is_ready:Boolean
    astarte:AstarteInterface
    introspection:any
    device_status:any
    device_setup:any
}

export const MainApp = ({is_ready, astarte, introspection, device_status, device_setup}:MainAppProps) => {
    const [current_temperature, set_temperature]    = React.useState<number>(0)
    const [current_consumption, set_consumption]    = React.useState<number>(0)
    const [current_vibration, set_vibration]        = React.useState<number>(0)
    const [current_efficiency, set_efficiency]      = React.useState<number>(0)
    const [current_setup, set_device_setup]         = React.useState<any>({})

    const OVERVIEW_K        = "OVERVIEW"
    const CHAMBER_TEMP_K    = "CHAMBER_TEMP"
    const PWR_CONSUMPTION_K = "PWR_CONSUMPTION"
    const ENGINE_VIBR_K     = "ENGINE_VIBR"

    const [selected_descriptor_key, set_descriptor_key] = React.useState<string>(OVERVIEW_K)
    const selectors_descriptors = {
        OVERVIEW_K  : {
            descriptor_id   : OVERVIEW_K,
            text            : "Overview",
            on_click        : (item:any) => {set_descriptor_key(OVERVIEW_K); console.log(item)}
        },
        CHAMBER_TEMP_K      : {
            descriptor_id   : CHAMBER_TEMP_K,
            text            : "Chamber Temperature",
            on_click        : (item:any) => {set_descriptor_key(CHAMBER_TEMP_K); console.log(item)}
        },
        PWR_CONSUMPTION_K   : {
            descriptor_id   : PWR_CONSUMPTION_K,
            text            : "Power Consumption",
            on_click        : (item:any) => {set_descriptor_key(PWR_CONSUMPTION_K); console.log(item)}
        },
        ENGINE_VIBR_K       : {
            descriptor_id   : ENGINE_VIBR_K,
            text            : "Engine Vibration",
            on_click        : (item:any) => {set_descriptor_key(ENGINE_VIBR_K); console.log(item)}

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
            set_efficiency(derive_efficiency(val["cahmberTemperature"], val["powerConsumption"], val["engineVibration"], current_setup))
        }
    }


    const on_app_ready  = () => {
        // Assigning initial values
        set_temperature(device_status['chamberTemperature'])
        set_consumption(device_status['powerConsumption'])
        set_vibration(device_status['engineVibration'])
        set_efficiency(derive_efficiency(current_temperature, current_consumption, current_vibration, current_setup))
        
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
            <Row>
                <Col sm={3} md={3}>
                    <Card className="shadow rounded">
                        <Card.Body>
                            <Nav variant="pills" defaultActiveKey={0}  className="flex-column">
                                {
                                    _.map(selectors_descriptors, (item:any, key:string, idx:number)=> {
                                        return (
                                            <Button key={key} className={`mt-2 text-start`}
                                                    value={item.descriptor_id} onClick={item.on_click}
                                                    variant={selected_descriptor_key == item.descriptor_id ? "info" : ""}>
                                                {item.text}
                                            </Button>
                                        )
                                    })
                                }
                            </Nav>
                        </Card.Body>
                    </Card>
                </Col>

                <Col sm={9} md={9}>
                    {
                        selected_descriptor_key == OVERVIEW_K ?
                            <StatusOverview temperature={current_temperature} consumption={current_consumption}
                                            vibration={current_vibration} efficiency={current_efficiency} />
                        :
                            <DetailedView />
                    }
                </Col>
            </Row>
        </Container>
    );
}