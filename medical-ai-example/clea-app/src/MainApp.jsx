
import "core-js/stable"
import "regenerator-runtime/runtime"
import React, { Fragment } from "react";
import RoomsOverview from "./components/RoomsOverview";
import HistroyBox from "./components/HistoryBox";
import RommDetails from "./components/RoomDetails";

import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, Spinner, Navbar, Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import Chart from "react-apexcharts";
import DatePicker from "react-datepicker";
import DatePickerStyle from "react-datepicker/dist/react-datepicker.css";
import _ from 'lodash';
import { render } from "react-dom";
import RoomDetails from "./components/RoomDetails";

// Global variables
let ROOMS_ITEMS_PER_ROW = 3;

// Global functions




export const MainApp = ({ astarteInterface, roomsList, introspection, isReady }) => {

    const deviceId                                      = astarteInterface.getDeviceId()
    const [roomsDescriptors, setRoomsDescriptors]       = React.useState ([])
    const [focusDescriptorIdx, setFocusDescriptorIdx]   = React.useState (0)


    const handleChannelEvent = (e) => {
        // TODO
    };




    React.useEffect(() => {
        if (isReady) {
            console.log (`Registering triggers and websockets for ${deviceId}..\n\nThis is the introspection:`)
            console.log (introspection)

            astarteInterface.getDeviceInformation()
            .then ((data) => {console.log (`Device info:`); console.log (data)})

            /* TODO
            astarteInterface.registerIncomingDataTrigger (handleChannelEvent, "com.astarte.Tester", "*", "/*")
            .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})*/

            // Setting up roomsDescriptors
            let tmpRdescriptors     = []
            let buildRoomDescriptor = (idx, text) => {
                return {
                    text                : text,
                    onclick             : (item) => {setFocusDescriptorIdx(idx)}
                }
            }

            tmpRdescriptors.push (buildRoomDescriptor (0, "Overview"))

            let initDescCount   = tmpRdescriptors.length
            _.map (roomsList, (item, idx) => {
                tmpRdescriptors.push (buildRoomDescriptor (initDescCount+idx, `Room ${item}`))
            })

            setRoomsDescriptors (tmpRdescriptors)
        }
    }, [isReady])
    
    
    
    return isReady==false ?
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
                        <Card>
                            <Card.Body>
                                <Nav variant="pills" defaultActiveKey="0" className="flex-column">
                                    {
                                        _.map (roomsDescriptors, (item, idx) => {
                                            return (
                                                <Button className='mt-2 text-start' value={item.value} onClick={item.onclick}
                                                        key={idx} variant={focusDescriptorIdx == idx ? "info" : ""}>
                                                    <span className="dot bg-success"/>      {/*bg-success    bg-danger*/}
                                                    {item.text}
                                                </Button>
                                            )
                                        })
                                    }
                                </Nav>
                            </Card.Body>
                        </Card>
                    </Col>

                    <Col sm={9} md={8}>
                        {focusDescriptorIdx == 0 ?
                        <Row>
                            <RoomsOverview descriptors={roomsDescriptors.slice(1)} itemsPerRow={ROOMS_ITEMS_PER_ROW}></RoomsOverview>
                        </Row> : 
                        
                        <Row>
                            <RoomDetails></RoomDetails>
                        </Row>
                        }



                        <Row>
                            <Card bg="info" className="counter-section rounded">
                                <Card.Body >
                                    <div className="counter-container text-center">
                                        <div className="counter-title">
                                            Statistics table...
                                        </div>
                                    </div>
                                </Card.Body>
                            </Card>
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