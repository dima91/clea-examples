
import React from "react";
import { Button, Card, Container, Spinner, Table } from "react-bootstrap";
import { Event, patientStatusToDescriptionString, patientStatusToStringColor, RoomDescriptor, stringToPatientStatus } from "./commons";
import moment from "moment";


type HistoryBoxProps = {
    events              : Array<Event>
    selectedRoomIdx     : Number
    focusDescriptorIdx  : Number
    roomsDescriptors    : Array<RoomDescriptor>
};

type ButtonDescriptor = {
    char    : String
    pageIdx : Number | undefined
    onClick : () => void
}


const computeShownPageRange = (minPage:number, maxPage:number, currPage:number, pageDelta:number) : number[] => {
    let lPage   = minPage
    let rPage   = lPage+pageDelta*2;
    rPage       = rPage<=maxPage ? rPage : maxPage
        while (lPage+pageDelta<currPage){
            lPage++;
            rPage++;
        }
        if (maxPage-currPage<=pageDelta) {
            rPage   = maxPage
            lPage   = (rPage-pageDelta*2)-1
            lPage   = rPage<=maxPage ? lPage : minPage
        }


    return [lPage, rPage]
}


const HistoryBox : React.FC<HistoryBoxProps> = ({events, selectedRoomIdx, focusDescriptorIdx, roomsDescriptors}) => {
    
    const ITEMS_PER_PAGE        = 8
    const START_PAGE            = 0
    const BUTTONS_PAGES_DELTA   = 2
    
    let [focusedPageIndex, setFocusedPageIndex] = React.useState (START_PAGE)
    let revEvents : Event[]                     = []
    let patientMap : Map<number, number>        = new Map()
    let roomEvents : Map<number, Event[]>       = new Map()
    let computeDuration                         = (curr:Event, prev:Event) => {
        let ms      = prev.timestamp-curr.timestamp
        /*console.log (`computeduration`)
        console.log (curr)
        console.log (prev)*/
        const res   = {
            hours   : Math.floor(ms / 3600000),
            minutes : Math.floor(ms / 60000) % 60,
            seconds : Math.floor(ms / 1000) % 60
        };
        const numberToString    = (n:number) => `${n <=9?'0':''}${n}`
        
        return `${numberToString(res.hours)}:${numberToString(res.minutes)}:${numberToString(res.seconds)} h`
    }
    let buildRow                                = (item:Event, prevItem:Event|undefined, idx:number, rowClassName:string) => {
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
                    <td>{evts.length>1 ? computeDuration (item, evts[evts.indexOf(item)-1]) : '-'}</td>
                    <td>{item.confidence ? item.confidence : `-`}</td>
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
                    <td>{prevItem!=undefined ? computeDuration (item, prevItem) : '-'}</td>
                    <td>{item.confidence ? item.confidence : `-`}</td>
                </tr>
            )
        }
        else {
            console.log (`Dropping item`)
            return <></>
        }
    }
    let integerDivision                         = (a:number, b:number) => Math.floor (a/b) + (a%b==0?0:1)
    let buttonsDescriptors : ButtonDescriptor[] = [
        {
            char    : '<',
            pageIdx : undefined,
            onClick : () => {setFocusedPageIndex((oldV) => oldV>0 ? oldV-1 : oldV)}
        },
        {
            char    : '>',
            pageIdx : undefined,
            onClick : () => {setFocusedPageIndex((oldV) => oldV<pagesCount-1 ? oldV+1 : oldV)}
        }
    ]
    
    events?.map( (item, idx, array) => {
        if (selectedRoomIdx == -1 || selectedRoomIdx == item.roomId)
        revEvents.unshift(item)
    })
    
    let pagesCount  = integerDivision (revEvents.length, ITEMS_PER_PAGE)
    for (let i=0; i<pagesCount; ++i) {
        buttonsDescriptors.splice (i+1, 0, {
            char    : (i+1).toString(),
            pageIdx : i,
            onClick : () => {setFocusedPageIndex(i)}
        })
    }
    
    let [MIN_PAGE, MAX_PAGE]  = computeShownPageRange (0, buttonsDescriptors.length-2, focusedPageIndex, BUTTONS_PAGES_DELTA)
    
    
    roomsDescriptors.map ((v, i, a) => {
        patientMap.set (v.roomId, v.patientId)
        roomEvents.set (v.roomId, [])
    })
    
    React.useEffect (() => {
        setFocusedPageIndex (START_PAGE)
    }, [selectedRoomIdx])
    
    /*console.log (`==========    Rerendering`)
    console.log (selectedRoomIdx)
    console.log (focusDescriptorIdx)
    console.log (roomsDescriptors)
    console.log (patientMap)
    console.log (`Displaying ${revEvents.length} events`)*/

    
    return (
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
                                            // Displaying current events only if belongs to visualized page
                                            let minIdx  = focusedPageIndex*ITEMS_PER_PAGE
                                            let maxIdx  = minIdx+ITEMS_PER_PAGE-1
                                            if (minIdx<=idx && idx<=maxIdx) {
                                                //console.log (`${minIdx} -> ${maxIdx} (${idx})`)
                                                return buildRow (item, (idx==0?undefined:array[idx-1]), idx, "mt-1 mb-1 row-style align-middle")
                                            }
                                            else
                                                return <></>
                                        }  catch {
                                            console.log (`Catched error at index ${idx}`)
                                            return <></>
                                        }
                                    })}
                                    </tbody>
                                </Table>

                                <div className="d-flex justify-content-end">
                                    {buttonsDescriptors.map ((item, idx, arr) => {
                                        let nIdx    = idx-1;                                        

                                        return item.pageIdx == undefined || (MIN_PAGE <= nIdx && nIdx <= MAX_PAGE) ?
                                        (
                                            <Button className="btn-circle shadow ml-4 mr-2"
                                                            variant={nIdx == focusedPageIndex ? 'primary' : 'light'}
                                                            onClick={item.onClick}>
                                                {item.char}
                                            </Button>
                                        )
                                        :
                                        <></>
                                    })}
                                </div>
                            </Card.Body>
                        )
                    }

                </Container>
            </Card>
        </Container>
    );
};

export default HistoryBox;
