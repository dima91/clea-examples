
import React from "react";
import { Card, Col, Container, Form, Row, Image } from "react-bootstrap";
import { RoomDescriptor, Event, stringToPatientStatus, patientStatusToGradientClass, patientStatusToDatailsTitle, patientStatusToDatailsBody, PatientStatus, normalizeConfidence } from "./commons";
import moment from "moment";


type RoomDetailsProps = {
    descriptor  : RoomDescriptor
};


const RoomDetails : React.FC<RoomDetailsProps> = ({descriptor}) => {
    
    let patientStatus   = stringToPatientStatus (descriptor.currentEvent.eventType)
    let startigDate     = moment (descriptor.currentEvent.timestamp)
    let hDate           = moment (descriptor.patientHospitalizationDate)
    let rDate           = moment (descriptor.patientReleaseDate)
    
    console.log (`Rendering this room (#${descriptor.roomId})`)
    console.log (descriptor)


    let getPatientImage = (e:Event) : React.ReactNode => {
        try {
            let s   = stringToPatientStatus (e.eventType)
        
            if (s != PatientStatus.NORMAL) {
                if (e.initFrameURL != undefined && e.initFrameURL.length!=0)
                    return (<Image
                                className="mt-4 d-flex justify-content-center shadow rounded w-100"
                                src={e.initFrameURL}/>)
            }
        } catch {
            return <></>
        }
    }

    let getEventConfidence  = (e: Event): React.ReactNode => {
        if (e.confidence != undefined)
            return <div className="d-flex justify-content-end align-text-bottom room-details-date">
                        Inference Confidence: {normalizeConfidence(e.confidence)*100}%
                    </div>
    }

    return (<>
    <Container fluid>
        <Row>
            <Col sm={6} md={6} lg={6}>
                <Card className="rounded h-100">
                    <Container fluid>
                        <Card.Subtitle className="mt-3 text-primary">
                            Details
                        </Card.Subtitle>
                        <Card.Body>
                            <Row>
                                {/* Patient ID*/}
                                <Col>
                                    <Form.Label className="fw-bold">Patient ID</Form.Label>
                                    <Form.Control
                                        readOnly
                                        placeholder={descriptor.patientId.toString()}
                                    />
                                </Col>
                            </Row>
                            <Row className="mt-3">
                                <Col sm={6} md={6}>
                                    <Form.Label className="fw-bold">Hospitalization date</Form.Label>
                                    <Form.Control
                                        readOnly
                                        placeholder={`${hDate.format('DD/MM/YY')}`}
                                    />
                                </Col>
                                <Col sm={6} md={6}>
                                    <Form.Label className="fw-bold">Release date</Form.Label>
                                    <Form.Control
                                        readOnly
                                        placeholder={`${rDate.format('DD/MM/YY')}`}
                                    />
                                </Col>
                            </Row>
                            <Row className="mt-3">
                            <Col sm={12}>
                                    <Form.Label className="fw-bold">Diagnosis</Form.Label>
                                    <Form.Control
                                        readOnly
                                        placeholder={descriptor.diagnosis.length>0 ? descriptor.diagnosis : "Unknown"}
                                    />
                                </Col>
                            </Row>
                        </Card.Body>
                    </Container>
                </Card>
            </Col>
            <Col sm={6} md={6} lg={6}>
                <Card className={`rounded ${patientStatusToGradientClass(patientStatus)} h-100`}>
                    <Container fluid className="h-100 text-white">
                        <Card.Subtitle className="mt-3">
                            Real time
                        </Card.Subtitle>
                        <Card.Title className="mt-2 room-details-title">
                            
                        </Card.Title>
                        <Card.Body className="">
                            <div className="room-details-title mt-1">{patientStatusToDatailsTitle(patientStatus)}</div>

                            <div>{patientStatusToDatailsBody(patientStatus)}</div>
                            {getPatientImage(descriptor.currentEvent)}
                            
                            {/* Bottom part */}
                            <div className="d-flex justify-content-end align-text-bottom room-details-date mt-4">
                                Date: {startigDate.format('DD/MM/YY, HH:mm:SS')}
                            </div>
                            {getEventConfidence(descriptor.currentEvent)}
                        </Card.Body>
                    </Container>
                </Card>
            </Col>
        </Row>
    </Container>
    </>);
};

export default RoomDetails;
