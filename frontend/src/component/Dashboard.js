// Fanfictions.js
import React, {useEffect} from 'react';
import NavbarComponent from './Navbar';
import Row from 'react-bootstrap/Row';
//import RowCard from './RowCards'
import Container from 'react-bootstrap/Container';
//import Col from 'react-bootstrap/Col';
import CardComp from './cardComp';




export default function Dashboard(props) {

    useEffect(() => {
    },[]);


  return (
    <div style={{paddingTop:25}}>
        <Container>
            <Row style={{paddingBottom:50}}>
                <NavbarComponent setIsLoggedIn={props.setIsLoggedIn}/>
            </Row>
        </Container>
        <CardComp/>

    </div>
  );
}
