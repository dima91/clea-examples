
import React from "react";
import {Container, Col, Row, Card, Nav, Button, Spinner} from "react-bootstrap";
import _ from "lodash";

import AstarteInterface from "../../commons/AstarteInterface"
import OverviewView from "./components/overview_view"
import ProductView from "./components/product_view"


type MainAppProps   = {
    is_ready                : boolean
    astarte                 : AstarteInterface
    introspection           : any
}


export const MainApp : React.FC<MainAppProps> = ({is_ready, astarte, introspection}:MainAppProps) => {

    const LAST_REFILL_EVENTS_COUNT                  = 50

    const [internal_ready, set_internal_ready]      = React.useState<boolean>(false)

    const OVERVIEW_DESCRIPTOR_KEY                   = "overview"
    const [selected_descriptor, set_descriptor_key] = React.useState<string>("undefined")
    const [selectors_descriptors, set_descriptors]  = React.useState<any[]>([])

    const [device_setup, set_device_setup]          = React.useState<any>(undefined)
    const [sales_prod_details, set_sales_details]   = React.useState<any>(undefined)
    const [last_refill_events, set_refill_events]   = React.useState<any>(undefined)
    const [products_details, set_prouct_details]    = React.useState<any>(undefined)

    // Obtaining initial values
    React.useEffect(() => {
        astarte.get_device_setup()
        .then((data) => {
            console.log(`device_setup`)
            console.log(data)
            set_device_setup(data)
        })
    }, [astarte])
    React.useEffect(() => {
        astarte.get_sales_product_details()
        .then((data) => {
            console.log(`sales_prod_details`)
            console.log(data)
            set_sales_details(data)
        })
    }, [astarte])
    React.useEffect(() => {
        astarte.get_product_details()
        .then((data) => {
            console.log(`products_details`)
            console.log(data)
            set_prouct_details(data)
        })
    }, [astarte])
    React.useEffect(() => {
        astarte.get_last_refill_events(LAST_REFILL_EVENTS_COUNT)
        .then((data) => {
            console.log('last_refill_events')
            console.log(data)
            set_refill_events(data)
        })
    }, [astarte])


    const build_selector                = (p_details:any) : any => {
        console.log(p_details)
        return {
            "display"   : p_details['name'],
            "key"       : p_details['ID'],
            onclick     : (evt:any) => {set_descriptor_key(p_details['ID'])}
        }
    }
    const get_selector_text_color       = (id:string, selected_id:string) => {
        if (id == selected_id)
            return "text-white"
        else
            return ""
    }
    const get_selector_bg_color         = (id:string, selected_id:string) => {
        if (id == selected_id)
            return "primary-bg"
        else
            return ""
    }


    const handle_channel_event = (evt:any) => {
        
        if (evt['event']['interface'] == astarte.sale_product_details_interface) {
            set_sales_details((val:any) => {
                let val_list    = evt['event']['path'].split('/')
                val[val_list[1]][val_list[2]]   = evt['event']['value']
                return val
            })
        }
    }


    React.useEffect (() => {
        if (!is_ready || !device_setup || !sales_prod_details || !last_refill_events || !products_details)
            return ;

        set_internal_ready(true)
        build_app()

        astarte.register_incoming_data_trigger (handle_channel_event, astarte.refill_event_interface, "*", "/*")
               .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
        astarte.register_incoming_data_trigger (handle_channel_event, astarte.sale_product_details_interface, "*", "/*")
               .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
    }, [is_ready, internal_ready, device_setup, sales_prod_details, last_refill_events, products_details])


    const build_app = ()=>{

        // Creating overview descriptor
        let overview_descriptor:any = {
            "display"   : "Overview",
            "key"       : OVERVIEW_DESCRIPTOR_KEY,
            onclick     : (evt:any) => {set_descriptor_key(OVERVIEW_DESCRIPTOR_KEY)}
        }
        set_descriptors([overview_descriptor])
        
        // Creating products descriptor
        let shown_products  = device_setup['device']['shownProducts']
        for (let i in shown_products) {
            let prod_key    = shown_products[i]
            let p_details   = products_details[prod_key]
            /*set_descriptors((curr_desc) => {
                curr_desc.push(build_selector(p_details))
                return curr_desc
            })*/
        }
        set_descriptor_key(OVERVIEW_DESCRIPTOR_KEY)
    }


    return (
        <Container fluid>
            {
                internal_ready == true ?
                    <Row>
                        <Col sm={3} md={3}>
                            <Card className="shadow rounded">
                                <Card.Body>
                                    <Nav variant="pills" defaultActiveKey={selected_descriptor}  className="flex-column">
                                        {
                                            _.map(selectors_descriptors, (item:any, key:number, idx:number)=> {
                                                return (
                                                    <Button key={key} value={item.descriptor_id} onClick={item.onclick}
                                                            className={`mt-2 text-start ${get_selector_text_color(item["key"], selected_descriptor)}
                                                                                        ${get_selector_bg_color(item["key"], selected_descriptor)}`}
                                                            variant={selected_descriptor == item['key'] ? "info" : ""}>
                                                        {item.display}
                                                    </Button>
                                                )
                                            })
                                        }
                                    </Nav>
                                </Card.Body>
                            </Card>
                        </Col>

                        <Col sm={9} md={9}>
                            {
                                _.map(selectors_descriptors, (item:any, key:number, idx:number) => {
                                    if (item['key']==selected_descriptor) {
                                        if (item['key']==OVERVIEW_DESCRIPTOR_KEY)
                                            return <OverviewView key={key} astarte={astarte} products_details={products_details} last_refill_events={last_refill_events} sale_products_details={sales_prod_details}/>
                                        else {
                                            return <ProductView key={key}/>
                                        }
                                    }
                                })
                            }
                        </Col>
                    </Row>
                :
                    <Row className="d-flex justify-content-center">
                        <Spinner className="m-5" animation="border" role="status" variant="Info">
                            <span className="visually-hidden">Loading...</span>
                        </Spinner>
                    </Row>
            }
        </Container>
    )
};


export default MainApp;