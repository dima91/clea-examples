
import _ from "lodash";
import React from "react";
import { Card, Table } from "react-bootstrap";


type RoomsOverviewProps = {
    descriptors : Array<Object>,
    itemsPerRow : number
};


const RoomsOverview : React.FC<RoomsOverviewProps>  = ({descriptors, itemsPerRow}) => {
    
    let currIdx = 0

    let groupedDescriptors  = _.reduce (descriptors, (acc : Array<Object>, item) => {
        if (currIdx % itemsPerRow == 0) {
            acc.push (descriptors.slice (currIdx, currIdx+itemsPerRow))
        }
        currIdx++
        return acc
    }, [])


    return (
        <Table responsive>
            <tbody>
                {
                    _.map (groupedDescriptors, (gitem, gidx) => {
                        console.log (gidx)
                        console.log (gitem)
                        let content = _.map (gitem, (item, idx) => {
                            console.log (`New key: ${gidx}${idx}`)
                            return (
                                <td key={`${gidx}${idx}`}>
                                    <Card>
                                        <div>realtime</div>
                                        <div>{item.text}</div>
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
