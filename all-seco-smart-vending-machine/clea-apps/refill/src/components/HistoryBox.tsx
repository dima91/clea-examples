
import React from "react";
import { Button, Card, Container, Spinner, Table, ThemeProvider } from "react-bootstrap";
import moment from "moment";


type HistoryBoxProps = {
    events              : Array<any>
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


const HistoryBox : React.FC<HistoryBoxProps> = ({events}) => {
    
    const ITEMS_PER_PAGE        = 8
    const START_PAGE            = 0
    const BUTTONS_PAGES_DELTA   = 2
    
    let [focusedPageIndex, setFocusedPageIndex] = React.useState (START_PAGE)
    
    const buildRow                              = (item:any, idx:any, row_class_name:string) => {
        return (
            <tr key={`key${idx}`} className={row_class_name}>
                <td>{moment(item['timestamp']).format("DD/MM/YYYY")}</td>
                <td>{item['refillerID']}</td>
                <td>{item['note']}</td>
            </tr>
        )
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
    
    let pagesCount  = integerDivision (events.length, ITEMS_PER_PAGE)
    for (let i=0; i<pagesCount; ++i) {
        buttonsDescriptors.splice (i+1, 0, {
            char    : (i+1).toString(),
            pageIdx : i,
            onClick : () => {setFocusedPageIndex(i)}
        })
    }
    
    let [MIN_PAGE, MAX_PAGE]  = computeShownPageRange (0, buttonsDescriptors.length-2, focusedPageIndex, BUTTONS_PAGES_DELTA)

    
    return (
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
                                    {
                                        (<tr className="mb-3" key='header'>
                                            <th>Date</th>
                                            <th>Refiller</th>
                                            <th>Note</th>
                                        </tr>)
                                    }
                                    </thead>

                                    <tbody>
                                    {events.map((item, idx, collection) => {
                                        try {
                                            console.log (item)
                                            // Displaying current events only if belongs to visualized page
                                            let minIdx  = focusedPageIndex*ITEMS_PER_PAGE
                                            let maxIdx  = minIdx+ITEMS_PER_PAGE-1
                                            if (minIdx<=idx && idx<=maxIdx) {
                                                return buildRow (item, idx, "mt-1 mb-1 row-style align-middle")
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
    );
};

export default HistoryBox;
