
import React from "react";
import { Card, Container, Spinner, Col, Navbar, ButtonToolbar, ToggleButton, Button } from "react-bootstrap";
import moment from "moment";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import DatePicker from "react-datepicker";
import {FaRegCalendarAlt} from 'react-icons/fa';
import  "../../node_modules/react-datepicker/dist/react-datepicker.css";
import AstarteInterface from "../../../commons/AstarteInterface";
import _, { result } from 'lodash';

// import * as DPStyle from "../../node_modules/react-datepicker/dist/react-datepicker.css";


type GetDataCallback        = (astarte:AstarteInterface, since:moment.Moment, to:moment.Moment) => any;
type DataFilterCallback     = (items:any) => any;
type ChartCardProps = {
    astarte : AstarteInterface,
    chart_name : string,
    data_retriever_cb : GetDataCallback
    data_filter_cb      : DataFilterCallback 
}


const y_axis_formatter  = (val:number, opt:any) => {
    return `${(val).toFixed(2)} %`
}
const months                        = [`Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sept`, `Oct`, `Nov`, `Dec`]



export const OverviewChartCard : React.FC<ChartCardProps> = ({astarte, chart_name, data_retriever_cb, data_filter_cb}:ChartCardProps) => {
    
    
    const MS_IN_24_HOURS                = 3600000
    const UPDATES_INTERVAL_DELAY_MS     = 10000

    const [date_range, set_date_range]  = React.useState([new Date(moment().valueOf() - MS_IN_24_HOURS), new Date()]);
    let chart_container_reference       = React.useRef<HTMLInputElement>(null)
    const [chart_desc, set_chart_desc]  = React.useState({width:0, height:0, raw_data:undefined})
    let updates_interval:any            = undefined

    const [selected_period, set_period] = React.useState<number>(0)
    const period_selectors              = [
        {name:"Day", value:0},
        {name:"Week", value:1},
        {name:"Month", value:2},
        {name:"Year", value:3}
        // Value 4 for calendar
    ]
    const chart_options : ApexOptions   = {
        chart: {
            id: 'statistics',
            type: 'line',
            stacked: false,
            zoom: {
                type: 'x',
                enabled: false,
                autoScaleYaxis: true
            },
            toolbar: {
                show: false
            }
        },
        stroke: {
            width: [3, 3],
            curve: 'smooth'
        },
        colors: ['#2E93fA', '#66DA26'],
        markers: {
            size: 0,
        },
        legend: {
            position:'bottom',
            horizontalAlign: 'left'
        },
        tooltip: {
            y: [
                {
                    formatter: y_axis_formatter
                }
            ],
            x: {
                formatter:(val:any) => {
                    let d       = new Date (val)
                    let addZero = (digit:number) => {
                        return (digit<10 ? `0${digit}` : `${digit}`)
                    }
                    let time    = `${addZero(d.getHours())}:${addZero(d.getMinutes())}`
    
                    return `${d.getDate()} ${months[d.getMonth()]} @ ${time}`
                }
            }
        },
        xaxis: {
            type: 'datetime',
            labels : {
                datetimeUTC: false
            }
        },
        yaxis: [
            {
                seriesName: chart_name,
                title: {
                  text: chart_name,
                    style: {
                        color: "#2E93fA"
                    }
                },
                axisBorder: {
                    show: true,
                    color: "#2E93fA"
                },
                labels: {
                    style: {
                        colors: "#2E93fA"
                    }
                },
            }
        ]
    }


    const resize_chart  = () => {
        if (chart_container_reference.current) {
            const domRect   = chart_container_reference.current.getBoundingClientRect()
            let newWidth    = domRect.width
            let newHeight   = domRect.height*3
            console.log (`w: ${newWidth}\th:${newHeight}`)
            set_chart_desc (desc  => {
                return {...desc, width:newWidth, height:newHeight}
            })
        }
    }

    const get_range_from_period = () => {
        let ed  = moment()
        let sd  = moment()
        switch (selected_period) {
            case 0:
                sd.subtract(1,'day'); break;
            case 1:
                sd.subtract(1, 'week'); break;
            case 2:
                sd.subtract(1, 'month'); break;
            case 3:
                sd.subtract(1, 'year'); break;
            default:
                throw `Wrong selected period! ${selected_period}`
        }
        
        return [new Date(sd.valueOf()), new Date(ed.valueOf())]
    }

    const update_date_range = (range:any) => {

        let sd  = undefined
        let ed  = undefined

        if (range==undefined) {
            let res = get_range_from_period()
            sd  = res[0]
            ed  = res[1]
        }

        else {
            let copyCurrTime    = (source:any) => {
                let d   = new Date()
                source.setHours (d.getHours())
                source.setMinutes (d.getMinutes())
                source.setSeconds (d.getSeconds())
                source.setMilliseconds (d.getMilliseconds())
                return source
            }

            sd  = new Date(range[0])
            ed  = null

            sd  = copyCurrTime (new Date(range[0]))
            if (range[1]) {
                ed  = copyCurrTime (new Date(range[1]))
            }
        }
        set_date_range ([sd, ed])
    }

    const range_to_string   = () => {
        let startDateString = date_range[0] ? date_range[0].toDateString() : "";
        let endDateString   = date_range[1] ? date_range[1].toDateString() : "";
        return `${startDateString}   -   ${endDateString}`
    }


    React.useEffect(() => {
        if (chart_container_reference.current) {

            window.addEventListener("resize", resize_chart);
            resize_chart();

            // Returning clean up function
            return () => {
                window.removeEventListener("resize", resize_chart, false);
            }
        }
    }, [chart_container_reference])


    React.useEffect(() => {

        // Registering data fetcher intervals
        if (!updates_interval) {
            console.log ("Registering updates interval")
            clearInterval(updates_interval)
            updates_interval    = setInterval(() => {
                console.log (`I'm into. selected period: ${selected_period}`)
                if (selected_period!=4)
                    update_date_range(undefined)
            }, UPDATES_INTERVAL_DELAY_MS)
        }

        console.log ("Im an effect!")

        if (selected_period!=4)
            update_date_range(undefined)

        return () => {clearInterval(updates_interval);updates_interval=undefined}
    }, [selected_period])


    React.useEffect(() => {
        // Checking if data retrieval is needed
        if (selected_period == 4) {
            console.log ("Calendar view selected")
            return;
        }

        console.log (`Retrieving data from ${date_range[0]} to ${date_range[1]}`)
        data_retriever_cb(astarte, moment(date_range[0].getTime()), moment(date_range[1].getTime()))
        .then ((response:any) => {
            console.log (_.isArray(response.data.data))
            set_chart_desc (curr_desc => {
                return {...curr_desc, raw_data:response.data.data}
            })
        })
    }, [date_range])



    const DataChart = () => {

        console.log ("DATACHART!!")
        console.log (chart_desc)
    
        if (!chart_desc.raw_data) {
            return (
                <Spinner className="m-5 d-flex justify-content-center" animation="border" role="status" variant="Info">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            );
        }
    
        const series    = React.useMemo(() => {
            let result  = []
            if (_.isArray(chart_desc.raw_data)) {
                // let filtered_data   = _.map(chart_desc.raw_data, (item:any, idx:number) => {return [new Date(item.timestamp), item.engineVibration]})
                let filtered_data   = data_filter_cb(chart_desc.raw_data)
                result.push ({
                    name    : chart_name,
                    data    : filtered_data
                })
            }

            return result
        }, [chart_desc.raw_data])
    
        return (
            <ReactApexChart type="line" width={chart_desc.width} height={chart_desc.height} options={chart_options} series={series}></ReactApexChart>
        )
    }




    return (
    <Card className="m-2 shadow">
        <Card.Body>
            {/*PERIOD SELECTORS*/}
            <ButtonToolbar className="d-flex justify-content-end m-2">
                <Navbar className="bg-light rounded">
                    {period_selectors.map((el, idx) => (
                        <ToggleButton variant='light' className={`ms-2 me-2 ${el.value==selected_period?'shadow text-primary' : 'text-dark'}`}
                                        key={idx} id={idx.toString()} type='radio' value={el.value} checked={el.value === selected_period}
                                        onChange={(evt) => {set_period(el.value);}}>
                                {el.name}
                        </ToggleButton>)
                    )}
                </Navbar>

                {/*DATE PICKER*/}
                <div>
                    <style>../../node_modules/react-datepicker/dist/react-datepicker.css</style>
                    <DatePicker
                        selectsRange={true}
                        startDate={date_range[0]}
                        endDate={date_range[1]}
                        onChange= {update_date_range}
                        className="ms-5"
                        customInput={
                            <Button variant={`light ${selected_period==4 ? 'shadow text-primary' : 'text-dark'}`}
                                    className="d-flex align-items-center m-3">
                                <FaRegCalendarAlt size={25} onClick={()=>{set_period(4)}}/>
                            </Button>
                        }
                    />
                </div>
            </ButtonToolbar>

            <div className="d-flex justify-content-end pe-3 fs-6">
                {range_to_string()}
            </div>
            
            
            <Container fluid className="d-flex justify-content-center" ref={chart_container_reference}>
                <Col sm={12} md={12}>
                    <DataChart/>
                </Col>
            </Container>
        </Card.Body>
    </Card>
    )
};


export default OverviewChartCard;