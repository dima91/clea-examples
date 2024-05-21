
import React from 'react'
import CSS from "csstype"
import { Link, useMatch } from 'react-router-dom'


export type MenuLinkProps = {
    title:  string;
    path: string;
  };

const MenuLink: React.FC<MenuLinkProps> = ({ title, path }) => {
    const match = useMatch(path)

    const linkStyle: CSS.Properties = {
        color:  match ? "#11b0ef" : "white",
        textDecoration: "none"
      }
    const textStyle: CSS.Properties = { 
        color: match ? "white" : "#abb0ba",
        fontSize: "16px",
        fontWeight: "650"
    }
    const cardBodyStyle: CSS.Properties = {
        //backgroundColor: match ? "#11b0ef" : "white",
        //borderColor: "white",
        //borderRadius: "10px",
        borderColor: "white"
    }
    const cardBackground : string = match!==null ? "bg-primary" : ""
    const cardMargin : string = match!==null ? " mt-1 mb-1 " : ""
    console.log (`${path} : ${match} -> ${match!==null}`)

    return (
        <div className='card-body p-1'>
            <div className={'card ' + cardBackground + cardMargin} style={cardBodyStyle}>
                <Link style={linkStyle} to={path}>
                    <p className='card-text ms-2 p-1' style={textStyle}>
                        {title}
                    </p>
                </Link>
            </div>
        </div>
    )
}

export default MenuLink;
