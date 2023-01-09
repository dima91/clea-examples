
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
    // FIXME Live events aren't considered!
    // TODO Implement pagination

    const ITEMS_PER_PAGE    = 8
    const START_PAGE        = 0

    let revEvents : Event[]                     = []
    let patientMap : Map<number, number>        = new Map()
    let roomEvents : Map<number, Event[]>       = new Map()
    let computeDuration                         = (curr:Event, prev:Event) => {
        let ms      = prev.timestamp-curr.timestamp
        const res   = {
            hours   : Math.floor(ms / 3600000) % 24,
            minutes : Math.floor(ms / 60000) % 60,
            seconds : Math.floor(ms / 1000) % 60
        };
        const numberToString    = (n:number) => `${n <=9?'0':''}${n}`
        
        return `${numberToString(res.hours)}:${numberToString(res.minutes)}:${numberToString(res.seconds)} h`
    }
    let buildRow                                = (item:Event, idx:number, rowClassName:string) => {
        //console.log (item)

        let status  = stringToPatientStatus (item.eventType)
        let evts    = roomEvents.get(item.roomId)
        if (evts==undefined)
            throw (`Events array for room #${item.roomId} is undefined`)
        evts.push (item)

        if (selectedRoomIdx == -1) {
            return (
                <tr className={rowClassName} key={`key${idx}`}>
                    <td>{item.roomId}</td>
                    <td>
                        <span className={`dot ${patientStatusToStringColor(status)}`}/>
                        {patientStatusToDescriptionString(status)}
                    </td>
                    <td>{moment(item.timestamp).format("DD/MM/YY - HH:mm:ss")}</td>
                    <td>{evts.length>1 ? computeDuration (item, evts[evts.length-2]) : '-'}</td>
                    <td>{item.confidence ? item.confidence : `UNKNOWN`}</td>
                    <td>{patientMap.get(item.roomId)}</td>
                </tr>
            )
        }
        else if (selectedRoomIdx == item.roomId) {
            return (
                <tr className={rowClassName} key={`key${idx}`}>
                    <td>{patientMap.get(item.roomId)}</td>
                    <td>
                        <span className={`dot ${patientStatusToStringColor(status)}`}/>
                        {patientStatusToDescriptionString(status)}
                    </td>
                    <td>{moment(item.timestamp).format("DD/MM/YY - HH:mm:ss")}</td>
                    <td>{evts.length>1 ? computeDuration (item, evts[evts.length-2]) : '-'}</td>
                    <td>{item.confidence ? item.confidence : `UNKNOWN`}</td>
                </tr>
            )
        }
        else
            return <></>
    }

    events?.map( (item, idx, array) => {
        revEvents.unshift(item)
    })

    roomsDescriptors.map ((v, i, a) => {
        patientMap.set (v.roomId, v.patientId)
        roomEvents.set (v.roomId, [])
    })

    console.log (`==========    Rerendering`)
    console.log (selectedRoomIdx)
    console.log (focusDescriptorIdx)
    console.log (roomsDescriptors)
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
                                {focusDescriptorIdx == -1 ?
                                    (<tr className="mb-3" key='header'>
                                        <th>Room</th>
                                        <th>Status</th>
                                        <th>Date</th>
                                        <th>Duration</th>
                                        <th>Confidence</th>
                                        <th>Patient ID</th>
                                    </tr>) :
                                    (<tr className="mb-3" key='header'>
                                        <th>Patient ID</th>
                                        <th>Status</th>
                                        <th>Date</th>
                                        <th>Duration</th>
                                        <th>Confidence</th>
                                    </tr>)
                                }
                                </thead>

                                <tbody>
                                {revEvents.map((item, idx, array) => {
                                    try {
                                        return buildRow (item, idx, "mt-1 mb-1")
                                    }  catch {
                                        return <></>
                                    }
                                })}
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
