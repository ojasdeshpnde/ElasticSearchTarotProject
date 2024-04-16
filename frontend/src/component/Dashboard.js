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
import ModalPopup from './Modal';
import { getBackendIP } from '../service/localhostSettings';
import OverlaySVG from './OverlaySVG';



export default function Dashboard(props) {

  const [getInit, setInit] = useState(false);
  const [formBool, setFormBool] = useState(false);
  const [boardSize, setBoardSize] = useState(0);
  const [board, setBoard] = useState([]);
  //const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    for(let i = 0; i < board.length; i++){
      console.log(board[i]);
    }
    if(!getInit){
      const getRe = async () => {
        const response = await fetch(getBackendIP() + '/get_reading', {
          method: 'GET',
          credentials:'include',
        });
        if(response.ok){
          console.log("running useEffect")
          response.json().then(data => {
            let tmpS = ['card1','card2','card3','card4','card5','card6','card7'];
            let tmpB = [];
            for(let i = 0 ; i < 7; i++){
              console.log(data[tmpS[i]].id >= 0);
              if(data[tmpS[i]].id >= 0){
                tmpB.push(<OverlaySVG key={data[tmpS[i]].id} text={data[tmpS[i]].text1} text2={data[tmpS[i]].text2} img = {'http://localhost:5002/getcard/'+data[tmpS[i]].image}/>);
              }
            }
            setBoard(tmpB);
            for(let i = 0; i < board.length; i++){
              console.log(board[i]);
            }
            setInit(true);
          });
        }
      }
      const resp = getRe().catch(console.error);
    }
    console.log(board);
    
  },[board]);


  return (
    <div style={{paddingTop:0, backgroundColor:"#c1a785"}}>
        <Container>
            <Row style={{paddingBottom:10}}>
                <NavbarComponent setIsLoggedIn={props.setIsLoggedIn}/>
            </Row>
            <ModalPopup board={board} setBoard={setBoard} show={formBool} setShow={setFormBool}/>
            <div style={{display:"grid", gridTemplateColumns:"auto auto auto auto" , paddingTop:100}}>
              {board}
              <AddCardComp setFormBool={setFormBool} boardSize={boardSize} setBoardSize={setBoardSize}/>
            </div>
        </Container>
        {/*<SearchBar setImg={setImg}/>*/}
        
        {/*<CardComp img={img}/>*/}    
        

    </div>
  );
}
