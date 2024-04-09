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



export default function Dashboard(props) {

  const [img, setImg] = useState();
  const [formBool, setFormBool] = useState(false);
  const [boardSize, setBoardSize] = useState(0);
  const [board, setBoard] = useState([]);
  //const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    for(let i = 0; i < board.length; i++){
      console.log(board[i]);
    }
     const getRe = async () => {
      const response = await fetch(getBackendIP() + '/get_reading', {
        method: 'GET',
        credentials:'include',
      });
      if(response.ok){
        response.json().then(data => {
          setBoard(
            [<CardComp key={data['card1'].id} text={data['card1'].text1} text2={data['card1'].text2} img = {'http://localhost:5002/getcard/'+data['card1'].image}/>,
            <CardComp key={data['card2'].id} text={data['card2'].text1} text2={data['card2'].text2}  img = {'http://localhost:5002/getcard/'+data['card2'].image}/>,
            <CardComp key={data['card3'].id} text={data['card3'].text1} text2={data['card3'].text2}  img = {'http://localhost:5002/getcard/'+data['card3'].image}/>,
            <CardComp key={data['card4'].id} text={data['card4'].text1} text2={data['card4'].text2}   img = {'http://localhost:5002/getcard/'+data['card4'].image}/>,
            <CardComp key={data['card5'].id} text={data['card5'].text1} text2={data['card5'].text2}  img = {'http://localhost:5002/getcard/'+data['card5'].image}/>,
            <CardComp key={data['card6'].id} text={data['card6'].text1}  text2={data['card6'].text2} img = {'http://localhost:5002/getcard/'+data['card6'].image}/>,
            <CardComp key={data['card7'].id} text={data['card7'].text1}  text2={data['card7'].text2} img = {'http://localhost:5002/getcard/'+data['card7'].image}/>
            ]);
          for(let i = 0; i < board.length; i++){
            console.log(board[i]);
          }
        });
      }
    }
    const resp = getRe().catch(console.error);
    
  },[]);


  return (
    <div style={{paddingTop:0}}>
        <Container>
            <Row style={{paddingBottom:10}}>
                <NavbarComponent setIsLoggedIn={props.setIsLoggedIn}/>
            </Row>
            <ModalPopup setBoard={setBoard} show={formBool} setShow={setFormBool}/>
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
