// Fanfictions.js
import React, {useEffect, useState} from 'react';
import NavbarComponent from './Navbar';
import Row from 'react-bootstrap/Row';
//import RowCard from './RowCards'
import Container from 'react-bootstrap/Container';
//import Col from 'react-bootstrap/Col';
import CardComp from './cardComp';
import SearchBar from './Search';
import AddCardComp from './AddCard';




export default function Dashboard(props) {

  const [img, setImg] = useState();

  const [boardSize, setBoardSize] = useState(0);
  const [board, setBoard] = useState([]);
  //const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const arr = [];
    for(let i = 0; i < boardSize; i++){
      arr.push(<CardComp key={i} img = {'http://localhost:5002/testimage'}/>);
    }
    setBoard(arr);
    fetch('http://localhost:5002/',{
      method: 'GET',
      credentials: 'include'});
  },[boardSize]);


  return (
    <div style={{paddingTop:0}}>
        <Container>
            <Row style={{paddingBottom:10}}>
                <NavbarComponent setIsLoggedIn={props.setIsLoggedIn}/>
            </Row>
            <div style={{display:"grid", gridTemplateColumns:"auto auto auto auto" , paddingTop:100}}>
              {board}
              <AddCardComp boardSize={boardSize} setBoardSize={setBoardSize}/>
            </div>
        </Container>
        {/*<SearchBar setImg={setImg}/>*/}
        
        {/*<CardComp img={img}/>*/}    
        

    </div>
  );
}
