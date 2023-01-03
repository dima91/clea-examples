
import "core-js/stable"
import "regenerator-runtime/runtime"
import React from "react";
import RoomsOverview from "./components/RoomsOverview";
import HistoryBox from "./components/HistoryBox";
import RoomDetails from "./components/RoomDetails";
import { patientStatusToStringColor, stringToPatientStatus } from "./components/commons";

import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, Spinner, Navbar, Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import Chart from "react-apexcharts";
import DatePicker from "react-datepicker";
import DatePickerStyle from "react-datepicker/dist/react-datepicker.css";
import _ from 'lodash';
import { render } from "react-dom";

// Global variables
const ROOMS_ITEMS_PER_ROW   = 3;
const ROOMS_OVERVIEW_IDX    = -1;

// Global functions




export const MainApp = ({ astarteInterface, roomsList, introspection, isReady }) => {

    const deviceId                                      = astarteInterface.getDeviceId()
    const [roomsDescriptors, setRoomsDescriptors]       = React.useState ([])
    const [focusDescriptorIdx, setFocusDescriptorIdx]   = React.useState (1)


    const handleChannelEvent = (e) => {
        // TODO
    };




    React.useEffect(async () => {
        if (isReady) {
            console.log (`Registering triggers and websockets for ${deviceId}..\n\nThis is the introspection:`)
            console.log (introspection)

            astarteInterface.getDeviceInformation()
            .then ((data) => {console.log (`Device info:`); console.log (data)})

            // Setting up roomsDescriptors
            let tmpRdescriptors     = []
            let buildRoomDescriptor = (descIdx, astarteDescriptor) => {

                if (descIdx == ROOMS_OVERVIEW_IDX) {
                    return {
                        descriptorId    : descIdx,
                        onclick         : (item) => {setFocusDescriptorIdx(descIdx)}
                    }
                }

                return {
                    descriptorId                : descIdx,
                    roomId                      : astarteDescriptor.roomId,
                    patientId                   : astarteDescriptor.patientId,
                    currentEvent                : astarteDescriptor.currentEvent,
                    diagnosis                   : astarteDescriptor.diagnosis,
                    patientHospitalizationDate  : astarteDescriptor.patientHospitalizationDate,
                    patientReleaseDate          : astarteDescriptor.patientReleaseDate,
                    onclick                     : (item) => {setFocusDescriptorIdx(descIdx)}
                }
            }

            tmpRdescriptors.push (buildRoomDescriptor (ROOMS_OVERVIEW_IDX, undefined))

            let astarteDescriptors  = []
            for (let i=0; i<roomsList.length;i++) {
                astarteDescriptors.push(astarteInterface.getRoomDetails (roomsList[i]))
            }

            let initDescCount   = tmpRdescriptors.length
            for (let i=0; i<astarteDescriptors.length; i++) {
                let d   = await (astarteDescriptors[i])
                console.log (`d`)
                console.log (d)
                tmpRdescriptors.push (buildRoomDescriptor (initDescCount+i, d))
            }

            setRoomsDescriptors (tmpRdescriptors)

            /* TODO
            astarteInterface.registerIncomingDataTrigger (handleChannelEvent, "com.astarte.Tester", "*", "/*")
            .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})*/
        }
    }, [isReady])
    
    
    
    return roomsDescriptors.length == 0 ?
    (
        <div className="p-4">
            <Container fluid className="text-center">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                    </Spinner>
            </Container>
        </div>
    ) :
    (
        <div className="p-4">
            <Container fluid>
                <Row>
                    {/* Overview buton + Rooms buttons */}
                    <Col sm={3} md={4}>
                        <Card className="shadow rounded">
                            <Card.Body>
                                <Nav variant="pills" defaultActiveKey="0" className="flex-column">
                                    {
                                        _.map (roomsDescriptors, (item, idx) => {
                                            console.log (`Rendering item #${idx}`)
                                            console.log (item)
                                            
                                            return (
                                                <Button className='mt-2 text-start' value={item.value} onClick={item.onclick}
                                                        key={idx} variant={focusDescriptorIdx == item.descriptorId ? "info" : ""}>
                                                    {item.descriptorId == ROOMS_OVERVIEW_IDX ?
                                                        <></> :
                                                        <span className={`dot ${patientStatusToStringColor(stringToPatientStatus(item.currentEvent.eventType))}`}/> }
                                                    <span className={focusDescriptorIdx == item.descriptorId ? "text-white" : ""}>
                                                        {item.descriptorId == ROOMS_OVERVIEW_IDX ? "Overview" : `Room ${item.roomId}`}
                                                    </span>
                                                </Button>
                                            )
                                        })
                                    }
                                </Nav>
                            </Card.Body>
                        </Card>
                    </Col>

                    <Col sm={9} md={8}>
                        {focusDescriptorIdx == ROOMS_OVERVIEW_IDX ?
                        <Row>
                            <RoomsOverview descriptors={roomsDescriptors.slice(1)} itemsPerRow={ROOMS_ITEMS_PER_ROW}></RoomsOverview>
                        </Row> : 
                        
                        <Row>
                            <RoomDetails></RoomDetails>
                        </Row>
                        }



                        <Row>
                            <HistoryBox/>
                        </Row>
                    </Col>
                </Row>

                {/* <Row className="mt-5">
                    <InputGroup className="mb-2">
                        <Row>
                            <InputGroup.Text>Counter</InputGroup.Text>
                            <InputGroup.Text>Random</InputGroup.Text>
                            <InputGroup.Text>Timestamp</InputGroup.Text>
                        </Row>
                    </InputGroup>
                </Row> */}
            </Container>
        </div>
    );
}