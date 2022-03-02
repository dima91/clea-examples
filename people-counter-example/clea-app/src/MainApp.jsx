
import "core-js/stable"
import "regenerator-runtime/runtime"
import React, { Fragment } from "react";
import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, 
            Navbar,
            Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import Chart from "react-apexcharts";
import DatePicker from "react-datepicker";
import DatePickerStyle from "react-datepicker/dist/react-datepicker.css";
import _, { now } from 'lodash';

let historical_data_size        = 5;            // minutes
const default_areas             = [];           // item : {zone_count, zone_name, zone_id}
let historical_data_cache       = [];           // item : {timestamp, value}
let last_query_date             = undefined;




export const MainApp = ({ sceneSettings, updateInterval, astarteClient, deviceId }) => {
    const chartRef              = React.useRef(null);
    const inputRef              = React.useRef(null);
    const [isReady, setIsReady] = React.useState(false);
    const [viz, setViz]         = React.useState({ width: 550, height: 350, data: [] });        // Right part: graph
    const [counter, setCounter] = React.useState({ total: 0, areas: default_areas });           // left part: counters
    

    const update_viz_and_stats  = (new_data) => {
        let current_timestamp   = new Date().getTime()

        // Checking if there are information
        if (!new_data || new_data.length == 0) {
            console.warn ("Empty data")
            return ;
        }

        // Updating historical_data_cache
        _.map (new_data, (d) => {
            if (d && d.timestamp!=undefined) {
                historical_data_cache.push ({timestamp: d.timestamp, value:d.people_count})
            }
        })
        // Removing too old data
        let delta_time_limit    = historical_data_size*60*1000
        while (current_timestamp - new Date(historical_data_cache[0].timestamp).getTime() > delta_time_limit) {
            historical_data_cache.shift();
        }

        // Updating counters with newest data
        let newest_data = new_data[new_data.length-1]
        if (newest_data)
            setCounter (parseCounterData(newest_data))

        // Updating chart with incoming data
        setViz (viz => {
            let new_viz = {
                width   : getChartWidth(),
                height  : viz.height,
                data    : _.map (historical_data_cache, (h) => {
                    return h
                })
            }
            
            return new_viz
        })
    }
    

    const getChartWidth = () => {
        if (isReady) {
            const domRect = chartRef.current.getBoundingClientRect();
            return domRect.width;
        }
        return 550;
    }


    const onHistoricalDataSizeUpdate    = (evt) => {
        if (inputRef.current && inputRef.current.value && !Object.is(parseInt(inputRef.current.value), NaN)
            && parseInt(inputRef.current.value) > 0) {
            historical_data_size    = parseInt (inputRef.current.value)

            let recent_data_since   = new Date();
            recent_data_since.setMinutes(last_query_date.getMinutes() - historical_data_size);

            getData (deviceId, astarteClient, undefined, recent_data_since)
            .then ((data) => {

                // Check performed to avoid strange rendering of chart
                if (historical_data_cache.length != 0)
                    historical_data_cache   = []
                
                // Updating chart with recent data
                update_viz_and_stats (data)
            })
        }
    }


    React.useEffect(() => {
        if (sceneSettings.length > 0) {
            
            // Setting up scene_zones
            _.map (sceneSettings, (d) => {
                let item    = {
                    zone_count  : 0,
                    zone_name   : d.zone_name,
                    zone_id     : d.zone_id
                }
                default_areas[item.zone_id] = item
            })

            let mount               = true;
            let interval_id         = undefined

            last_query_date         = new Date();
            let recent_data_since   = new Date();
            recent_data_since.setMinutes(last_query_date.getMinutes() - historical_data_size);

            getData (deviceId, astarteClient, undefined, recent_data_since)
            .then ((data) => {
            
                // Check performed to avoid strange rendering of chart
                if (historical_data_cache.length != 0)
                    data    = []
                
                // Updating chart with recent data
                update_viz_and_stats (data)
                

                // Creating periodic task that fetch and update data
                interval_id = setInterval(() => {
                    if (mount) {
                        // Querying data only from last update
                        getData(deviceId, astarteClient, undefined, last_query_date)
                        .then((data) => {
                            last_query_date         = new Date();
                            
                            if (!data || data.length==0) {
                                return;
                            }

                            update_viz_and_stats (data)
                        })
                    }
                }, updateInterval);
            })

            return () => {
                if (interval_id) {
                    console.warn ("Clearing interval...")
                    clearInterval(interval_id);
                }
                mount = false;
            }
        }
    }, [sceneSettings, updateInterval, deviceId, astarteClient]);


    React.useEffect(() => {
        if (chartRef.current) {
            setIsReady(true);
        }
    }, [chartRef]);


    React.useEffect(() => {
        if (isReady) {
            const resizeChart = () => {
                const domRect = chartRef.current.getBoundingClientRect();
                setViz(viz => {
                    return { ...viz, width: domRect.width }
                });
            }
            window.addEventListener("resize", resizeChart);

            return () => {
                window.removeEventListener("resize", resizeChart, false);
            }
        }
    }, [isReady]);


    return (
        <div className="p-4">
            <Container fluid>
                <Row>
                    <Col sm={12} md={6}>
                        <Card bg="info" className="counter-section rounded">
                            <Card.Body>
                                <div className="counter-container">
                                    <div className="counter-title">
                                        <small>Real time</small>
                                        <h3>People Counter</h3>
                                    </div>
                                    <div className="counter-number">
                                        {counter.total}
                                    </div>
                                </div>
                            </Card.Body>
                        </Card>
                        <Row>
                            {counter.areas.map((area, index) => {
                                return (
                                    <Col sm={12} md={6} key={index}>
                                        <Card className="area-section rounded">
                                            <Card.Body>
                                                <div className="area-container">
                                                    <div className="area-title text-secondary">
                                                        <h4>{area.zone_name}</h4>
                                                        <small>People Counter</small>
                                                    </div>
                                                    <div className="area-number text-primary">
                                                        {area.zone_count}
                                                    </div>
                                                </div>
                                            </Card.Body>
                                        </Card>
                                    </Col>);
                            })}
                        </Row>
                    </Col>
                    <Col sm={12} md={6}>
                        <Card className="chart-section rounded">
                            <Card.Body>
                                
                                <InputGroup className="mb-3">
                                    <InputGroup.Text>Chart History Size</InputGroup.Text>
                                    <FormControl aria-label="Minutes" /*value={HISTORICAL_MINUTES_LIMIT}*/
                                                ref={inputRef}/>
                                    <Button variant="outline-secondary" id="history-update-id"
                                            onClick={onHistoricalDataSizeUpdate}>
                                        Update
                                    </Button>
                                </InputGroup>
                                
                                <div className="chart-container" ref={chartRef}>
                                    <Fragment>
                                        <DataChart width={viz.width} height={viz.height} data={viz.data} />
                                    </Fragment>
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </div>
    );
}




/*  =====================================
            ASTARTE DATA HANDLERS
    ===================================== */

async function getData(deviceId, astarteClient, limit, since) {
    return astarteClient
        .getCameraData({ deviceId, limit, since})
        .then((data) => {
            return data;
        })
        .catch(() => {
            return undefined;
        });
}


function parseCounterData(data) {
    /* RETURN VALUE : {
        total,
        timestamp,
        areas   : {
            zone_count,
            zone_name,
            zone_id
        }
    }*/

    let counter  = {
        total       : 0,
        timestamp   : new Date (data.timestamp),
        areas       : JSON.parse(JSON.stringify(default_areas))
    }

    const people    = data.people ? data.people : [];
    _.map (people, (person) => {
        let parsed_person   = JSON.parse (person)
        if (parsed_person.pos_zone.id in default_areas) {
            counter.areas[parsed_person.pos_zone.id].zone_count += 1
            counter.total++
        }
        else
            console.error (`Person ${parsed_person.id} has no correspondent area!`)
    })

    return counter;
}




/*  ==============================
            CHART SETTINGS
    ============================== */

const chartOptions = {
    chart: {
        id: 'people',
        type: 'line',
        stacked: false,
        zoom: {
            type: 'x',
            enabled: false,
            autoScaleYaxis: true
        },
        toolbar: {
            autoSelected: 'zoom'
        }
    },
    stroke: {
        width: [2, 2],
        curve: 'smooth'
    },
    colors: ['#FF8300'],
    dataLabels: {
        enabled: false
    },
    markers: {
        size: 0,
    },
    title: {
        text: 'People',
        align: 'left'
    },
    xaxis: {
        type: 'datetime',
    },
    tooltip: {
        shared: false,
        y: {
            formatter: function (val) {
                return (val).toFixed(0)
            }
        }
    },
    yaxis: {
        labels: {
            formatter: function (val) {
                return (val).toFixed(0);
            },
        },
    }
};


const DataChart = ({ data, width, height, isMount = false }) => {

    if (data.length === 0) {
        return (
            <div>
                <FormattedMessage id="no_data" defaultMessage="No recent data" />
            </div>
        );
    }

    const series = React.useMemo(
        () => {
            
            return [
                {
                    name: "People",
                    data: data.map((d) => [new Date(d.timestamp), d.value]),
                },
            ]
        },
        [data]
    );

    return (
        <Chart type="line" width={width} options={chartOptions} series={series} />
    );
};