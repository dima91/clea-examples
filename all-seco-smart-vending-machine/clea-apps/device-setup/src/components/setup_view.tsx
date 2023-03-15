
import React from "react"
import {Button, Col, Container, Form, FormControl, InputGroup, Row} from "react-bootstrap"

import _ from "lodash";
import AstarteInterface from "../../../commons/AstarteInterface";


export type UpdatedParamCallback    = (id:string, new_value:any) => void
export type SetupViewProps          = {
    astarte : AstarteInterface
}


export const SetupView : React.FC<SetupViewProps> = ({astarte} : SetupViewProps) => {

    const [current_setup, set_current_setup]            = React.useState<any>(undefined)
    const [current_status, set_current_status]          = React.useState<any>(undefined)
    const [is_ready, set_is_ready]                      = React.useState(false)

    React.useEffect (() => {
        astarte.get_last_device_status(1)
        .then ((data:any) => {
            set_current_status(data[0])
        })
    }, [astarte])
    React.useEffect (() => {
        astarte.get_device_setup()
        .then ((data:any) => {
            set_current_setup(data)
        })
    }, [astarte])
    React.useEffect(() => {
        console.log (`ready?`)
        console.log(current_setup)
        console.log(current_status)

        if (current_setup!=undefined && current_status!=undefined)
            set_is_ready(true)
    }, [current_setup, current_status])

    // TODO Registering to channels

    const build_row = (name:string, status:string|undefined, jsx_input:any) => {
        return <Row className="m-2">
            <Col sm={5} md={5}>{name}</Col>
            <Col sm={3} md={3}>{status}</Col>
            <Col sm={4} md={4}>{jsx_input}</Col>
        </Row>
    }


    // TODO Text Input builder
    const text_input_builder    = (on_change:UpdatedParamCallback, id:string) => {
        return (
            <Row>
                <Col sm={5} md={5}>
                    <Form.Control aria-label="Minutes" placeholder="25.8"/>
                </Col>
                <Col sm={3} md={3}>
                    <Button variant="secondary" id="history-update-id">
                        Apply
                    </Button>
                </Col>
            </Row>
        )
    }

    // TODO On/Off input builder
    const on_off_input_builder  = (start_value:boolean, on_change:UpdatedParamCallback, id:string) => {
        return (
            <Row>
                <Col sm={4} md={4}>
                <Form>
                    <Form.Check 
                        type="switch"
                        id="custom-switch"
                        label="Off"
                        checked={start_value}
                        onChange={(({target:{value}}) => {console.log(value)})}
                    />
                </Form>
                </Col>
            </Row>
        )
    }

    return (
        is_ready==true ?
            <Container>
                <Row>
                    <Row className="fw-bold m-2">
                        <Col sm={5} md={5}>
                            Parameters
                        </Col>
                        <Col sm={3} md={3}>
                            Status
                        </Col>
                        <Col sm={4} md={4}>
                            Setup
                        </Col>
                    </Row>


                    {/*Chamber temperature*/}
                    <Row>
                        <Col sm={5} md={5}>
                            Chamber temperature
                        </Col>
                        <Col sm={3} md={3}>
                            {current_status["chamberTemperature"]}
                        </Col>
                        <Col sm={4} md={4}>
                            <Row>
                                <Col sm={5} md={5}>
                                    <Form.Control aria-label="Minutes" placeholder="25.8" />
                                </Col>
                                <Col sm={3} md={3}>
                                    <Button variant="secondary" id="history-update-id" onClick={()=>{/*TODO*/}}>
                                        Apply
                                    </Button>
                                </Col>
                            </Row>
                        </Col>
                    </Row>


                    {/*Light output*/}
                    <Row>
                        <Col sm={5} md={5}>
                            Light output
                        </Col>
                        <Col sm={3} md={3}>
                            {current_setup['device']["lightOutput"]}
                        </Col>
                        <Row>
                        <Col sm={4} md={4}>
                        <Form>
                            <Form.Check 
                                type="switch"
                                id="custom-switch"
                                label="Off"
                                checked={current_setup['device']["lightOutput"]}
                                onChange={(evt) => {
                                    console.log (evt.target.value)
                                    let new_val = evt.target.value=="on"?false:true
                                    console.log (new_val)
                                    set_current_setup((v:any) => {v['device']['lightOutput']= new_val; return v;})
                                    // astarte.set_property("device/lightOutput", !current_setup['device']["lightOutput"])
                                    // .then(()=> {})
                                }}
                            />
                        </Form>
                        </Col>
                    </Row>
                    </Row>

                    {/*Light output*/}
                </Row>
            </Container>
        :
            <></>
        )
}