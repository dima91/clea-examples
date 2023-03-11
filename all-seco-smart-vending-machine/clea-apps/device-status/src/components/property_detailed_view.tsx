
import React from "react";
import AstarteInterface from "../../../commons/AstarteInterface";
import ChartCard from "./chart_card";


type GetDataCallback        = (astarte:AstarteInterface, since:moment.Moment, to:moment.Moment) => any;
type DataFilterCallback     = (items:any) => any;
type DetailedViewProps  = {
    astarte             : AstarteInterface
    chart_name          : string
    data_retriever_cb   : GetDataCallback
    data_filter_cb      : DataFilterCallback
}


export const DetailedView : React.FC<DetailedViewProps> = ({astarte, chart_name, data_retriever_cb, data_filter_cb}:DetailedViewProps) => {

    return <ChartCard astarte={astarte} chart_name={chart_name} data_retriever_cb={data_retriever_cb} data_filter_cb={data_filter_cb}/>
};


export default DetailedView