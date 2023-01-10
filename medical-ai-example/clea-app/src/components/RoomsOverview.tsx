
import _, { values } from "lodash";
import React from "react";
import { Card, Col, Row, Table } from "react-bootstrap";
import { RoomDescriptor, patientStatusToDescriptionString, stringToPatientStatus, patientStatusToGradientClass } from "./commons";


type CardClickCallback  =   (id:number) => void;
type RoomsOverviewProps = {
    descriptors : Array<RoomDescriptor>,
    itemsPerRow : number,
    onclick     : CardClickCallback
};


const RoomsOverview : React.FC<RoomsOverviewProps>  = ({descriptors, itemsPerRow, onclick}) => {
    // FIXME Prevent card dimension changing!
    
    let currIdx             = 0
    let groupedDescriptors  = []
    
    // Grouping descriptors
    for (currIdx = 0; currIdx<descriptors.length; currIdx++) {
        if (currIdx % itemsPerRow == 0) {
            groupedDescriptors.push (descriptors.slice (currIdx, currIdx+itemsPerRow))
        }
    }


    return (
        <Table responsive>
            <tbody>
                {
                    _.map (groupedDescriptors, (gitem, gidx) => {
                        let content = _.map (gitem, (room, idx) => {
                            let patientStatus   = undefined
                            try {
                                patientStatus   = stringToPatientStatus(room.currentEvent.eventType)
                            } catch {}
                            return (
                                <td key={`${gidx}${idx}`}>
                                    <Card className={`clickable-card rounded ${patientStatus!=undefined ? patientStatusToGradientClass(patientStatus) : ''}`}
                                            onClick={(it1) => {onclick(room.roomId)}}>
                                        <Card.Body className="text-white">
                                            <Row className="m-0 p-0 mb-1">
                                                    <div className="fs-10 m-0 p-0">Real time</div>
                                            </Row>
                                            <Row className="m-0 p-0">
                                                <Col className="fs-5 m-0 p-0">Room {room.roomId}</Col>
                                                {patientStatus != undefined ?
                                                    <Col className="text-end fs-4 m-0 p-0 patient-status-text">{patientStatusToDescriptionString(patientStatus)}</Col>
                                                : <></>}
                                            </Row>
                                        </Card.Body>
                                    </Card>
                                </td>
                            )
                        })
                        return (
                            <tr key={`${gidx}`}>
                                {content}
                            </tr>
                        )
                    })
                }
            </tbody>
        </Table>
    );
};

export default RoomsOverview;
