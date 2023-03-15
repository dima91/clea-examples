
import React from "react";
import { Container, Col, Row, Card, Nav, Button } from "react-bootstrap";
import _ from "lodash";

import AstarteInterface from "../../commons/AstarteInterface"
import {SetupView, UpdatedParamCallback as SetupParamCallback} from "./components/setup_view";
import {TriggerView, UpdatedParamCallback as TriggerParamCallback} from "./components/trigger_view"


type MainAppProps   = {
    is_ready        : boolean
    astarte         : AstarteInterface
    intrspection    : any
    device_setup    : any
    device_status   : any
}


export const MainApp : React.FC<MainAppProps> = ({is_ready, astarte, intrspection, device_setup, device_status}:MainAppProps) => {

    const [current_setup, set_current_setup]            = React.useState<any>(undefined)
    const [current_status, set_current_status]          = React.useState<any>(undefined)
    const [selected_descriptor_idx, set_descriptor_idx] = React.useState<number>(-1)

    React.useEffect(() => {
        console.log (`idx changed: ${selected_descriptor_idx}`)
    }, [selected_descriptor_idx])

    const selectors_descriptors :any = [
        {
            idx         : 0,
            text        : "Setup",
            onclick     : () => {set_descriptor_idx(0)},
            render_cb   : () => {
                                    console.log("Do something..")
                                    return (<SetupView astarte={astarte}/>)
                                }
        },
        {
            idx     : 1,
            text    : "Trigger",
            onclick : () => {set_descriptor_idx(1)},
            render_cb   : () => {
                                    console.log ("Do something else..")
                                    return (<TriggerView on_param_update={trigger_param_callback} current_setup={device_setup}
                                                            current_status={device_status}></TriggerView>)
                                }
        }
    ]

    const setup_param_callback : SetupParamCallback     = (id:string, new_value:any) => {
        // TODO Send info to Astarte
    }
    const trigger_param_callback : TriggerParamCallback = (id:string) => {
        // TODO Send info to Astarte
    }

    React.useEffect (() => {
        if (!is_ready)
            return ;

        set_descriptor_idx(0)
        set_current_setup(device_setup)
        set_current_status(device_status)

        build_app(device_setup, device_status)
    }, [is_ready])


    const build_app = (setup:any, status:any) => {
        console.log ("App ready! Initial settings:")
        console.log (device_setup)
        console.log (device_status)
    }
    
    
    return (
        <Container fluid>
            <Row>
                <Col sm={3} md={3}>
                    <Card className="shadow rounded">
                        <Card.Body>
                            <Nav variant="pills" defaultActiveKey={0}  className="flex-column">
                                {
                                    _.map(selectors_descriptors, (item:any, key:number, data:any)=> {
                                        return (
                                            <Button key={key} className={`mt-2 text-start ${selected_descriptor_idx==key ? "text-white" : ""}`}
                                                    value={key} onClick={item.onclick}
                                                    variant={selected_descriptor_idx == item.idx ? "info" : ""}>
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
                        _.map(selectors_descriptors, (item:any, key:number, data:any) => {
                            if (selected_descriptor_idx == key) {
                                return item.render_cb()
                            }
                        })
                    }
                </Col>
            </Row>
        </Container>
    )
};


export default MainApp;