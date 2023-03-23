
import React, { createElement } from "react";
import {Card, Row} from "react-bootstrap";
import {MapContainer, TileLayer} from "react-leaflet";

import Commons from "./Commons";


type MapCardProps   = {
}


export const MapCard : React.FC<MapCardProps>   = ({}) => {

    return (
        <Card>
            <style>{Commons.get_leaflet_style()}</style>

            <Row className="fs-8 fw-bold text-primary m-3">
                Map
            </Row>

            <MapContainer center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false} className="ms-3 me-3 mb-3">
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
            </MapContainer>
        </Card>
    )
}


export default MapCard;