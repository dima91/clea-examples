
import React from "react";
import {Card, Nav, Button} from "react-bootstrap";

import _ from 'lodash'

import Commons from "./Commons";


export type SelectorState        = {
    value   : string
    setter  : React.Dispatch<React.SetStateAction<string>>
}
export type SelectorDescriptor      = {
    key             : string
    display_string  : string
}
export type SelectorsListCardProps  = {
    selected_selector   : SelectorState
    descriptors         : Array<SelectorDescriptor>
}


const SelectorsListCard : React.FC<SelectorsListCardProps>  = ({selected_selector, descriptors}) => {

    


    const get_selector_text_color   = (current_key:string, selected_key:string) => {
        if (current_key == selected_key)
            return "text-white"
        else
            return ""
    }

    const get_selector_bg_color     = (current_key:string, selected_key:string) => {
        if (current_key == selected_key)
            return "primary-bg"
        else
            return ""
    }

    const on_item_click             = (evt:any, item:SelectorDescriptor) => {
        selected_selector.setter(item.key)
    }

    return (
        <Card className="shadow rounded">
            <Card.Body>
                <Nav variant="pills" defaultActiveKey={selected_selector.value}  className="flex-column">
                    {
                        _.map(descriptors, (item:SelectorDescriptor, key:number, idx:number)=> {
                            return (
                                <Button key={key} value={item.key} onClick={(evt:any) => on_item_click(evt, item)}
                                        className={`mt-2 text-start ${get_selector_text_color(item["key"], selected_selector.value)}
                                                                    ${get_selector_bg_color(item["key"], selected_selector.value)}`}
                                        variant={""}>
                                    {item.display_string}
                                </Button>
                            )
                        })
                    }
                </Nav>
            </Card.Body>
        </Card>
    )
}


export default SelectorsListCard