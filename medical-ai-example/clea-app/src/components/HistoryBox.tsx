
import React from "react";
import { Card, Container, Spinner, Table } from "react-bootstrap";
import { Event, patientStatusToDescriptionString, patientStatusToStringColor, RoomDescriptor, stringToPatientStatus } from "./commons";
import _ from "lodash";
import moment from "moment";
import { string } from "yup";


type HistoryBoxProps = {
    events              : Array<Event>
    selectedRoomIdx     : Number
    focusDescriptorIdx  : Number
    roomsDescriptors    : Array<RoomDescriptor>
};


const HistoryBox : React.FC<HistoryBoxProps> = ({events, selectedRoomIdx, focusDescriptorIdx, roomsDescriptors}) => {
    const ITEMS_PER_PAGE    = 8

    console.log (`==========    Rerendering`)
    console.log (selectedRoomIdx)
    console.log (roomsDescriptors)

    let patientMap : Map<number, number>    = new Map()

    roomsDescriptors.map ((v, i, a) => {
        patientMap.set (v.roomId, v.patientId)
    })

    console.log (patientMap)
    
    return (<>
    <Container fluid>
        <Card bg="light" className="rounded shadow mt-3 h-100">
            <Container fluid>

                <Card.Subtitle className="mt-3 text-primary">
                    History
                </Card.Subtitle>

                {
                    events==undefined ? 
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
                        <Card.Body>
                            <Table responsive hover size="sm" className="mt-2">
                                <thead>
                                    <tr className="mb-3" key='header'>
                                        <th>Room</th>
                                        <th>Status</th>
                                        <th>Date</th>
                                        <th>Duration</th>
                                        <th>Confidence</th>
                                        <th>Patient ID</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {
                                        events.reverse().map((item, idx, events) => {

                                            if (idx==0)
                                                return <></>

                                            if (selectedRoomIdx>0 && selectedRoomIdx!=item.roomId)
                                                return <></>

                                            try  {
                                                let status  = stringToPatientStatus (item.eventType)
                                                return (
                                                    <tr className="mt-1 mb-1" key={`evts${idx}`}>
                                                        <td>{item.roomId}</td>
                                                        <td>
                                                            <span className={`dot ${patientStatusToStringColor(status)}`}/>
                                                            {patientStatusToDescriptionString(status)}
                                                        </td>
                                                        <td>{moment(item.timestamp).format("DD/MM/YY - HH:mm:ss")}</td>
                                                        <td>?</td>
                                                        <td>{item.confidence}</td>
                                                        <td>?</td>
                                                    </tr>
                                                )
                                            }
                                            catch {
                                                return <></>
                                            }
                                        })
                                    }
                                </tbody>
                            </Table>
                        </Card.Body>
                    )
                }

            </Container>
        </Card>
    </Container>
    </>);
};

export default HistoryBox;
