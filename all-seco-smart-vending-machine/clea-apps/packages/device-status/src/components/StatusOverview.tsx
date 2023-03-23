
import React from "react"
import {Col, Row, Container, Card} from "react-bootstrap"

import _ from "lodash";

import AstarteInterface from "commons/AstarteInterface"
import Commons from "commons/Commons"
import ChartCard from "commons/ChartCard"
import GetDataCallback from "commons/ChartCard"
import DataFilterCallback from "commons/ChartCard"


type StatusOverviewProps = {
    astarte:AstarteInterface
    device_setup:any
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
        description : "There is a suspected increase of consumption and engine vibration to maintain the chamber temperature.\nRequest assistance to check temotor before it breaks down.",
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


const build_efficiency_details_card = (efficiency:number) => {
    let desc            = efficiency>=65 ? efficiency_descriptor["normal"] : efficiency_descriptor["warning"]
    //console.log (desc)

    return (
        <Card className={`rounded shadow m-2 text-white ${desc.bg}`}>
            <Card.Body>
            <Row className="fs-6">
                    <div>Predictive Maintenance</div>
                </Row>
                <Row>
                    <div className="fs-1 d-flex justify-content-center">{desc.title}</div>
                </Row>
                <Row className="mt-4">
                    <div className="fs-6 d-flex justify-content-center">{desc.description}</div>
                </Row>
            </Card.Body>
        </Card>
    )
}


export const StatusOverview : React.FC<StatusOverviewProps>  = ({temperature, consumption, vibration, efficiency, device_setup, astarte} : StatusOverviewProps) => {

    let data_retriever_cb = (a:AstarteInterface, s:moment.Moment, t:moment.Moment) => {
        return a.get_device_status_time_series(s,t)
    }

    let data_filter_cb    = (items:any) => {
        //let downsampled   = downsample(items, 30)
        return _.map(items, (it:any, idx:number) => {
            return [new Date(it.timestamp), Commons.derive_efficiency(it.chamberTemperature, it.powerConsumption,
                                                                        it.engineVibration, device_setup)]
        })
    }

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
                <Col sm={7}>
                    {/* <ChartCard astarte={astarte} chart_name={"Efficiency"}
                               data_retriever_cb={data_retriever_cb}
                               data_filter_cb={data_filter_cb}>
                    </ChartCard> */}
                    <ChartCard astarte={astarte} chart_name={"Efficiency"}
                                data_retriever_cb={data_retriever_cb} data_filter_cb={data_filter_cb}/>
                </Col>
                <Col sm={5}>{build_efficiency_details_card(efficiency)}</Col>
            </Row>
        </Container>
    )
};


export default StatusOverview;