
import "core-js/stable"
import "regenerator-runtime/runtime"
import React from "react";
import moment from 'moment';
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




export const MainApp = ({ astarteInterface, roomsList, introspection, isReady }) => {

    const ROOMS_ITEMS_PER_ROW   = 3;
    const ROOMS_OVERVIEW_IDX    = -1;
    
    const deviceId                                      = astarteInterface.getDeviceId()
    const [roomsDescriptors, setRoomsDescriptors]       = React.useState ([])
    const [focusDescriptorIdx, setFocusDescriptorIdx]   = React.useState (ROOMS_OVERVIEW_IDX)   // Index of selected room in roomDescriptors array
    const [selectedRoomIdx, setSelectedRoomIdx]         = React.useState (ROOMS_OVERVIEW_IDX)
    const [eventsList, setEventsList]                   = React.useState (undefined)
    const [tmpEvent, setTmpEvent]                       = React.useState ({})


    const handleChannelEvent = (e) => {
        /*console.log (`New event!!!`)
        console.log (e)*/
        let evt = e.event.value
        setEventsList ((prev) => {
            let newEvent    = {
                roomId              : evt.roomId,
                timestamp           : moment(e.timestamp).valueOf(),
                eventType           : evt.eventType,
                confidence          : evt.confidence,
                initFrameURL        : evt.initFrameURL,
                initFrameContent    : evt.initFrameContent
            }
            prev.push(newEvent);
            setTmpEvent (e)
            return prev;
        })
    };
    
    const onRoomsOverviewClick  = (id) => {
        let i   = 0
        while (i<roomsDescriptors.length && roomsDescriptors[i].roomId != id)
            i++
        if (i==roomsDescriptors.length)
            throw `[onRoomsOverviewClick] Cannot find room with id ${id}`
        
        return i
    }

    React.useEffect (() => {
        console.log (`Handling tmpEvent..`)
        
        if (tmpEvent && 'timestamp' in tmpEvent && 'event' in tmpEvent && 'value' in tmpEvent.event) {            
            let newEvent    = {
                timestamp           : moment (tmpEvent.timestamp).valueOf(),
                eventType           : tmpEvent.event.value.eventType,
                confidence          : tmpEvent.event.value.confidence,
                initFrameContent    : tmpEvent.event.value.initFrameContent,
                initFrameURL        : tmpEvent.event.value.initFrameURL,
                roomId              : Number(tmpEvent.event.path.slice(1))
            }

            // Updating event for target room
            let tmpRdescriptors = []
            for (let di in roomsDescriptors) {
                let d   = roomsDescriptors[di]
                if (d.roomId == newEvent.roomId) {
                    d.currentEvent  = newEvent 
                }

                tmpRdescriptors.push (d)
            }
            setRoomsDescriptors (tmpRdescriptors)
        }
    }, [tmpEvent])




    React.useEffect(async () => {
        if (isReady) {
            console.log (`Registering triggers and websockets for ${deviceId}..\n\nThis is the introspection:`)
            console.log (introspection)

            astarteInterface.getDeviceInformation()
            .then ((data) => {console.log (`Device info:`); console.log (data)})

            // Querying for global events
            let events  = astarteInterface.getLastEvents (8, undefined)

            // Setting up roomsDescriptors
            let tmpRdescriptors     = []
            let buildRoomDescriptor = (descIdx, astarteDescriptor) => {

                if (descIdx == ROOMS_OVERVIEW_IDX) {

                    return {
                        descriptorId    : descIdx,
                        onclick         : (item) => {setFocusDescriptorIdx(descIdx); setSelectedRoomIdx(descIdx)}
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
                    onclick                     : (item) => {   console.log (`Setting descriptor with ${descIdx}`);
                                                                setFocusDescriptorIdx(descIdx);
                                                                setSelectedRoomIdx(astarteDescriptor.roomId)}
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
                tmpRdescriptors.push (buildRoomDescriptor (initDescCount+i, d))
            }

            setRoomsDescriptors (tmpRdescriptors)

            // Awaiting for events list
            let evts    = await (events)
            setEventsList (evts)

            // Registering event handler
            astarteInterface.registerIncomingDataTrigger (handleChannelEvent, "it.unisi.atlas.Event6", "*", "/*")
            .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
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
                                            try {
                                                return (
                                                    <Button className='mt-2 text-start' value={item.value} onClick={item.onclick}
                                                            key={idx} variant={focusDescriptorIdx == item.descriptorId ? "info shadow" : ""}>
                                                        {item.descriptorId == ROOMS_OVERVIEW_IDX ?
                                                            <></> :
                                                            <span className={`dot ${patientStatusToStringColor(stringToPatientStatus(item.currentEvent.eventType))}`}/> }
                                                        <span className={focusDescriptorIdx == item.descriptorId ? "text-white" : ""}>
                                                            {item.descriptorId == ROOMS_OVERVIEW_IDX ? "Overview" : `Room ${item.roomId}`}
                                                        </span>
                                                    </Button>
                                                )
                                            } catch {
                                                return <></>
                                            }
                                        })
                                    }
                                </Nav>
                            </Card.Body>
                        </Card>
                    </Col>

                    <Col sm={9} md={8}>
                        {focusDescriptorIdx == ROOMS_OVERVIEW_IDX ?
                        <Row>
                            <RoomsOverview descriptors={roomsDescriptors.slice(1)} itemsPerRow={ROOMS_ITEMS_PER_ROW}
                                            onclick={(id)=>{
                                                setFocusDescriptorIdx(onRoomsOverviewClick(id))
                                                setSelectedRoomIdx(id)
                                            }}></RoomsOverview>
                        </Row> : 
                        
                        <Row>
                            <RoomDetails descriptor={roomsDescriptors[focusDescriptorIdx]}></RoomDetails>
                        </Row>
                        }



                        <Row>
                            <HistoryBox events={eventsList} selectedRoomIdx={selectedRoomIdx}
                                        focusDescriptorIdx={focusDescriptorIdx} roomsDescriptors={roomsDescriptors.slice(1)}/>
                        </Row>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}