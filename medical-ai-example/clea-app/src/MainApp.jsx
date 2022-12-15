
import "core-js/stable"
import "regenerator-runtime/runtime"
import React, { Fragment } from "react";
import { Button, Col, Container, Card, Row, InputGroup, FormControl, ToggleButton,
            ToggleButtonGroup, Spinner, Navbar, Nav} from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import Chart from "react-apexcharts";
import DatePicker from "react-datepicker";
import DatePickerStyle from "react-datepicker/dist/react-datepicker.css";
import _ from 'lodash';

// Global variables

// Global functions




export const MainApp = ({ publishInterval, astarteInterface, introspection, isReady }) => {
    const [counter, setCounter]     = React.useState(-1)
    const [random, setRandom]       = React.useState(-1)
    const [timestamp, setTimestamp] = React.useState(-1)

    const deviceId                  = astarteInterface.getDeviceId()

    const handleChannelEvent = (e) => {
        setCounter (e.event.value.counter)
        setRandom (e.event.value.random)
        setTimestamp (e.event.value.timestamp)
      };

    React.useEffect(() => {
        if (isReady) {
            console.log (`Registering triggers and websockets for ${deviceId}..\n\nThis is the introspection:`)
            console.log (introspection)

            astarteInterface.getDeviceInformation()
            .then ((data) => {console.log (`Device info:`); console.log (data)})

            astarteInterface.registerIncomingDataTrigger (handleChannelEvent, "com.astarte.Tester", "*", "/*")
            .then ((roomName) => {console.log (`Trigger created! The room is  ${roomName}`)})
        }
    }, [isReady])
    
    
    
    return (
        <div className="p-4">
            <Container fluid>
                <Row>
                    <Col sm={12} md={12}>
                        <Card bg="info" className="counter-section rounded">
                            <Card.Body >
                                <div className="counter-container text-center">
                                    <div className="counter-title">
                                        <small>Tester Publish Interval: {publishInterval} ms</small>
                                    </div>
                                </div>
                            </Card.Body>
                        </Card>
                        <Row>
                        </Row>
                    </Col>
                    <Col sm={12} md={6}>
                    </Col>
                </Row>

                <Row className="mt-5">
                    <InputGroup className="mb-2">
                        <Row>
                            <InputGroup.Text>Counter: {counter}</InputGroup.Text>
                            <InputGroup.Text>Random: {random}</InputGroup.Text>
                            <InputGroup.Text>Timestamp: {timestamp==-1 ? -1 : new Date(timestamp*1000).toLocaleString()} - ({timestamp})</InputGroup.Text>
                        </Row>
                    </InputGroup>
                </Row>
            </Container>
        </div>
    );
}