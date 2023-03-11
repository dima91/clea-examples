
import React from "react";
import { Card, Col, Container, Row } from "react-bootstrap";

import ChartCard from "./chart_card";


type StatusOverviewProps = {
    temperature:number,
    consumption:number,
    vibration:number,
    efficiency:number,
}


let efficiency_descriptor   = {
    "normal"    : {
        title       : "No warning",
        description : "This vending machine is in very good condition.\nPredicitive maintenance will alert you in time of any anomalies so you can schedule a technician's intervention.",
        bg          : "primary-bg"
    },
    "warning"   : {
        title       : "Warning",
        description : "This vending machine is in very good condition.\nPredicitive maintenance will alert you in time of any anomalies so you can schedule a technician's intervention.",
        bg          : "warning-gradient-bg"
    }
}


const build_card    = (text:string, value:string, unit:string) => {
    return (
        <Card className="rounded shadow text-white m-2 primary-bg">
            <Card.Body>
                <Row className="fs-6">
                    <div>Real time</div>
                </Row>
                <Row>
                    <Col className="fs-5 d-flex align-items-center" sm={6} md={6}>{text}</Col>
                    <Col className="text-end mb-0" sm={6} md={6}>
                        <span className="fs-1 font-weight-bold">{value}</span>
                        <span className="fs-5">{unit}</span>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}


const build_chart_card  = () => {
    return (
        <ChartCard></ChartCard>
    )
}


const build_efficiency_details_card = (efficiency:number) => {
    let desc            = efficiency>=65 ? efficiency_descriptor["normal"] : efficiency_descriptor["warning"]
    console.log (desc)

    return (
        <Card className={`rounded shadow m-2 text-white ${desc.bg}`}>
            <Card.Body>
            <Row className="fs-6">
                    <div>Predictive Maintenance</div>
                </Row>
                <Row>
                    <div className="fs-1 d-flex justify-content-center">{desc.title}</div>
                </Row>
                <Row>
                    <div className="fs-6 d-flex justify-content-center">{desc.description}</div>
                </Row>
            </Card.Body>
        </Card>
    )
}


export const StatusOverview : React.FC<StatusOverviewProps>  = ({temperature, consumption, vibration, efficiency} : StatusOverviewProps) => {

    return (
        <Container>
            <Row>
                <Col sm={6}>{build_card("Chamber Temperature", temperature.toString(), "°C")}</Col>
                <Col sm={6}>{build_card("Power consumption", consumption.toString(), "kWh")}</Col>
            </Row>
            
            <Row>
                <Col sm={6}>{build_card("Engine vibration", vibration.toString(), "kHz")}</Col>
                <Col sm={6}>{build_card("Device efficiency", efficiency.toString(), "%")}</Col>
            </Row>

            <Row>
                <Col sm={7}>{build_chart_card()}</Col>
                <Col sm={5}>{build_efficiency_details_card(efficiency)}</Col>
            </Row>
        </Container>
    )
};


export default StatusOverview;