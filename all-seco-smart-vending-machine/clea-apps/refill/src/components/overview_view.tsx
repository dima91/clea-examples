
import React from "react"
import {Button, Card, Col, Container, Form, FormControl, InputGroup, Row, ProgressBar} from "react-bootstrap"

import _ from "lodash";
import moment from "moment";
import AstarteInterface from "../../../commons/AstarteInterface";
import HistoryBox from "./HistoryBox";


export type OverviewViewProps       = {
    astarte                 : AstarteInterface
    products_details        : any,
    sale_products_details   : any,
    last_refill_events      : any
}

enum Status {
    NORMAL  = 0,
    WARNING = 1,
    DANGER  = 2
}


export const OverviewView : React.FC<OverviewViewProps> = ({astarte, products_details, sale_products_details, last_refill_events} : OverviewViewProps) => {

    const get_remaining_products    = (products:any) : number => {
        let result  = 0
        for (let i in products) {
            result += products[i]['remainingItems']
        }
        return result
    }
    const get_total_products        = (products:any) : number => {
        let result  = 0
        for (let i in products) {
            result += products[i]['maxItemsCount']
        }
        return result
    }
    const get_running_out_ptoduct   = (products:any) : string => {
        let id          = ""
        let min_count   = undefined
        for (let i in products) {
            let p   = products[i]
            if (min_count == undefined || p['remainingItems']<min_count) {
                min_count   = p['remainingItems']
                id          = i
                console.log (`${id} is the new minimum with ${min_count}`)
            }
        }
        return products_details[id]['name']
    }
    const get_last_refilled_date    = (refill_events:any) : string => {
        let last_date   = undefined
        console.log (refill_events)
        for (let i in refill_events) {
            let d = moment(refill_events[i]['timestamp'])
            if (last_date==undefined || d > last_date)
                last_date   = d
        }
        console.log(`Last date: ${last_date}`)
        return last_date==undefined ? "--/--" : last_date.format("MM/DD")
        
    }
    const get_percentage            = (max:number, curr_value:number) => {
        return max/100*curr_value
    }
    const percentage_to_status      = (percentage:number) : Status => {
        if (percentage>=.7)
            return Status.NORMAL
        else if (percentage>=.3)
            return Status.WARNING
        else
            return Status.DANGER
    }
    const status_to_variant         = (status:Status) => {
        if (status==Status.NORMAL)
            return "success"
        else if (status==Status.WARNING)
            return "warning"
        else
            return "danger"
    }


    const make_refill               = (evt:any) => {
        astarte.make_refill('-', (Math.random()*1000000).toFixed(0).toString())
    }


    const build_card                    = (title:string, description:string|undefined, value:string, sub_value:string|undefined) : any => {
        return (
            <Card className="primary-bg text-white m-1 p-2 shadow">
                <Row className="fs-6">
                    <div>{title}</div>
                </Row>
                <Row>
                    {
                        description!=undefined ?                         
                            <Col className="fs-5 d-flex align-items-center" sm={6} md={6}>{description}</Col>
                        :
                            <Col className="fs-5 d-flex align-items-center" sm={6} md={6}></Col>

                    }
                    <Col className="text-end mb-0" sm={6} md={6}>
                        <span className="fs-1 font-weight-bold">{value}</span>
                        {
                            sub_value!=undefined ?
                                <span className="fs-5">{sub_value}</span>
                            :
                            <span className="fs-5">{sub_value}</span>
                        }
                    </Col>
                </Row>
            </Card>
        )
    }


    const build_product_percentage_row      = (product_details:any, sale_details:any) : JSX.Element => {
        // console.log (sale_details)
        // console.log (`preparing row for product  ${product_details['name']}  qith value ${get_percentage(sale_details['maxItemsCount'], sale_details['remainingItems'])}`)
        let percentage  = get_percentage(sale_details['maxItemsCount'], sale_details['remainingItems'])
        let curr_status = percentage_to_status(percentage)
        return (
            <Row key={product_details['ID']} className="p-2">
                <Row>
                    <Col className="d-flex justify-content-start fw-bold">{product_details['name']}</Col>
                    <Col className="d-flex justify-content-end">{percentage*100}%</Col>
                </Row>
                <Row className="">
                    <Col>
                        <ProgressBar now={percentage*100} variant={status_to_variant(curr_status)}/>
                    </Col>
                </Row>
            </Row>
        )
    }


    const build_status_card_description     = (products_details:any, sale_details:any) : JSX.Element => {
        let min_percentage          = 10
        let min_percentage_product  = ""
        let mean                    = 0
        for (let p in sale_details) {
            let curr_perc   = get_percentage(sale_details[p]['maxItemsCount'], sale_details[p]['remainingItems'])
            mean           += curr_perc
            if (curr_perc<min_percentage) {
                min_percentage          = curr_perc
                min_percentage_product  = p
            }
        }
        let curr_status = percentage_to_status(min_percentage)
        mean            = mean/(Object.keys(sale_details).length)
        
        return (
            <Card className={`${curr_status == Status.NORMAL?"primary-bg":"warning-gradient-bg"} p-2 m-2 text-white`}>
                <Row className="fs-6">
                    <div>Refill Manager</div>
                </Row>

                <Row className="fs-1 p-2 m-2">
                    {curr_status == Status.NORMAL?"Not forthcoming":"Warning"}
                </Row>

                <Card.Body>
                    {
                        curr_status == Status.NORMAL?
                            <p>Vending machine is well stocked at the moment.
                                Refill is not necessary.</p>
                        :
                            <div>
                                <Row>
                                    <p>
                                    Products within vending machine are running out.
                                    According to the analysis of the sales trends, it is recommended to refill this vending machine within two days.
                                    </p>
                                </Row>

                                <Row className="d-flex align-items-baseline">
                                    <Col sm={6} md={6} className="d-flex justify-content-start align-items-baseline">
                                        <span>Remaining products</span>
                                    </Col>
                                    <Col sm={6} md={6} className="d-flex justify-content-end align-items-baseline">
                                        <span className="fs-2">{mean*100}</span>
                                        <span>%</span>
                                    </Col>
                                </Row>
                                
                                <Row className="d-flex align-items-baseline">
                                    <Col sm={6} md={6} className="d-flex justify-content-start align-items-baseline">
                                        <span>Suggested refill date</span>
                                    </Col>
                                    <Col sm={6} md={6} className="d-flex justify-content-end align-items-baseline">
                                        <span className="fs-2">{moment().add(2, "days").format("DD/MM/YY")}</span>
                                    </Col>
                                </Row>

                                <Row className="d-flex mt-4">
                                    <Col sm={6} md={6} className="d-flex justify-content-start align-items-baseline">
                                        <Button variant="outline-light" onClick={make_refill}>Refill now</Button>
                                    </Col>
                                    <Col sm={6} md={6} className="d-flex justify-content-end align-items-baseline">
                                        <Button variant="outline-light">Schedule refill</Button>
                                    </Col>
                                </Row>

                                
                            </div>
                    }
                </Card.Body>
            </Card>
        )
    }


    const build_refill_history_card         = (refill_history:any) => {
        console.log(`last_refill_events!!!!`)
        console.log(refill_history)
        return (
            <Card className="primary-text m-1 p-2 shadow fw-both">
                <Row>
                    <HistoryBox events={refill_history['refill'].reverse()}></HistoryBox>
                </Row>
            </Card>
        )
    }


    return (
        <Container fluid>
            <Row>
                <Col sm={4} md={4}>
                    {build_card("Products", "Remaining", get_remaining_products(sale_products_details).toString(), `/${get_total_products(sale_products_details).toString()}`)}
                </Col>
                <Col sm={4} md={4}>
                    {build_card("Running out", undefined, get_running_out_ptoduct(sale_products_details), undefined)}
                </Col>
                <Col sm={4} md={4}>
                    {build_card("Last date", "Refilled", get_last_refilled_date(last_refill_events['refill']), undefined)}
                </Col>
            </Row>

            <Row>
                <Col sm={7} md={7}>
                    <Card className="rounded shadow p-1 m-2">
                        <Row className="fs-6 fw-bold primary-text">
                            <div>Percentage products</div>
                        </Row>

                        <Card.Body>

                        {
                            _.map(products_details, (item:any, key:string, collection_any) => {
                                return build_product_percentage_row(item, sale_products_details[key])
                            })
                        }
                        </Card.Body>
                    </Card>
                </Col>

                <Col sm={5} md={5}>
                    {build_status_card_description(products_details, sale_products_details)}
                </Col>
            </Row>

            <Row>
                <Col sm={12} md={12}>
                    {build_refill_history_card(last_refill_events)}
                </Col>
            </Row>
        </Container>
    )
}


export default OverviewView;