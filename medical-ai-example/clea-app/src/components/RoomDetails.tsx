
import React from "react";
import { Card, Col, Container, Form, Row, Image } from "react-bootstrap";
import { RoomDescriptor, Event, stringToPatientStatus, patientStatusToGradientClass, patientStatusToDatailsTitle, patientStatusToDatailsBody, PatientStatus } from "./commons";
import moment from "moment";


type RoomDetailsProps = {
    roomDescriptor  : RoomDescriptor
};


const RoomDetails : React.FC<RoomDetailsProps> = ({roomDescriptor}) => {
    console.log (`Rendering this room (#${roomDescriptor.roomId})`)
    console.log (roomDescriptor)
    let patientStatus   = stringToPatientStatus (roomDescriptor.currentEvent.eventType)
    let startigDate     = moment (roomDescriptor.currentEvent.timestamp)
    let hDate           = moment (roomDescriptor.patientHospitalizationDate)
    let rDate           = moment (roomDescriptor.patientReleaseDate)


    let getPatientImage = (e:Event) : React.ReactNode => {
        let s   = stringToPatientStatus (e.eventType)
        
        if (s != PatientStatus.NORMAL) {
            if (e.initFrameURL != undefined && e.initFrameURL.length!=0)
                return (<Image
                            className="mt-4 d-flex justify-content-center shadow rounded"
                            src={e.initFrameURL}/>)
        }
    }

    let getEventConfidence  = (e: Event): React.ReactNode => {
        if (e.confidence != undefined)
            return <div className="d-flex justify-content-end align-text-bottom room-details-date">
                        Inference Confidence: {e.confidence*100}%
                    </div>
    }

    return (<>
    <Container fluid>
        <Row>
            <Col sm={6} md={6} lg={6}>
                <Card className="rounded shadow bg-light h-100">
                    <Container fluid>
                        {/* <Card.Title className='text-primary mt-3 fs-5'>
                            Details
                        </Card.Title> */}
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
                                        defaultValue={roomDescriptor.patientId}
                                    />
                                </Col>
                            </Row>
                            <Row className="mt-3">
                                <Col sm={6} md={6}>
                                    <Form.Label className="fw-bold">Hospitalization date</Form.Label>
                                    <Form.Control
                                        readOnly
                                        defaultValue={`${hDate.format('DD/MM/YY')}`}
                                    />
                                </Col>
                                <Col sm={6} md={6}>
                                    <Form.Label className="fw-bold">Release date</Form.Label>
                                    <Form.Control
                                        readOnly
                                        defaultValue={`${rDate.format('DD/MM/YY')}`}
                                    />
                                </Col>
                            </Row>
                            <Row className="mt-3">
                            <Col sm={12}>
                                    <Form.Label className="fw-bold">Diagnosis</Form.Label>
                                    <Form.Control
                                        readOnly
                                        defaultValue={roomDescriptor.diagnosis.length>0 ? roomDescriptor.diagnosis : "Unknown"}
                                    />
                                </Col>
                            </Row>
                        </Card.Body>
                    </Container>
                </Card>
            </Col>
            <Col sm={6} md={6} lg={6}>
                <Card className={`rounded shadow ${patientStatusToGradientClass(patientStatus)} h-100`}>
                    <Container fluid className="h-100 text-white">
                        <Card.Subtitle className="mt-3">
                            Real time
                        </Card.Subtitle>
                        <Card.Title className="mt-2 room-details-title">
                            
                        </Card.Title>
                        <Card.Body className="">
                            <div className="room-details-title mt-1">{patientStatusToDatailsTitle(patientStatus)}</div>

                            <div>{patientStatusToDatailsBody(patientStatus)}</div>
                            {getPatientImage(roomDescriptor.currentEvent)}
                            
                            {/* Bottom part */}
                            <div className="d-flex justify-content-end align-text-bottom room-details-date mt-4">
                                Date: {startigDate.format('DD/MM/YY, HH:mm:SS')}
                            </div>
                            {getEventConfidence(roomDescriptor.currentEvent)}
                        </Card.Body>
                    </Container>
                </Card>
            </Col>
        </Row>
    </Container>
    </>);
};

export default RoomDetails;
