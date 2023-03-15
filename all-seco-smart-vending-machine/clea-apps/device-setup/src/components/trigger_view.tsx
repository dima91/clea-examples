
import React from "react"
import {Container, Row, Col, Button, Form} from "react-bootstrap"


export type UpdatedParamCallback    = (id:string, new_value:any) => void
type TriggerViewProps = {
    on_param_update : UpdatedParamCallback
    current_setup   : any
    current_status  : any
}


export const TriggerView : React.FC<TriggerViewProps> = ({on_param_update, current_setup, current_status} : TriggerViewProps) => {

    const row_builder   = (param_name:string, current_status:string, jsx_input:any) => {

    }

    // TODO Text Input builder
    const text_input_builder    = (/*TODO on_change, param_id*/) => {
        return (
            <Row>
                <Col sm={4} md={4}>
                    <Form.Control aria-label="Minutes" defaultValue={0}/>
                </Col>
                <Col sm={3} md={3}>
                    <Button variant="secondary" id="history-update-id">
                        Apply
                    </Button>
                </Col>
            </Row>
        )
    }


    return (
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

            <>
                {row_builder("Max operating chamber temperature", current_setup["device"]["targetTemperature"], text_input_builder())}
            </>
        </Row>
    </Container>
    )
}