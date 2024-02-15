// Fanfictions.js
import React, {useEffect, useState} from 'react';
import NavbarComponent from './Navbar';
import Row from 'react-bootstrap/Row';
//import RowCard from './RowCards'
import Container from 'react-bootstrap/Container';
//import Col from 'react-bootstrap/Col';
import CardComp from './cardComp';
import SearchBar from './Search';




export default function Dashboard(props) {

  const [img, setImg] = useState();

    useEffect(() => {
    },[]);


  return (
    <div style={{paddingTop:25}}>
        <Container>
            <Row style={{paddingBottom:50}}>
                <NavbarComponent setIsLoggedIn={props.setIsLoggedIn}/>
            </Row>
        </Container>
        <SearchBar setImg={setImg}/>
        <CardComp img={img}/>

    </div>
  );
}
