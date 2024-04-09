import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import InputForm from './InputForm';
import { getBackendIP } from '../service/localhostSettings';
import CardComp from './cardComp';

function ModalPopup(props) {

  const handleClose = () => props.setShow(false);
  const handleShow = () => props.setShow(true);


  const [formObj, setFormObj] = useState({
    linkText:"",
    imgText:""
  });


  const handleSubmit = async () => {
    try {
        console.log("Submitting!!")
        const response = await fetch(getBackendIP() + '/store_reading', {
          method: 'POST',
          credentials:'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formObj),
        });

  
        if (response.ok) {
          console.log("success!!")
          response.json().then(data => {
            props.setBoard(
                [<CardComp key={data['card1'].id} text={data['card1'].text1} text2={data['card1'].text2} img = {'http://localhost:5002/getcard/'+data['card1'].image}/>,
                <CardComp key={data['card2'].id} text={data['card2'].text1} text2={data['card2'].text2}  img = {'http://localhost:5002/getcard/'+data['card2'].image}/>,
                <CardComp key={data['card3'].id} text={data['card3'].text1} text2={data['card3'].text2}  img = {'http://localhost:5002/getcard/'+data['card3'].image}/>,
                <CardComp key={data['card4'].id} text={data['card4'].text1} text2={data['card4'].text2}   img = {'http://localhost:5002/getcard/'+data['card4'].image}/>,
                <CardComp key={data['card5'].id} text={data['card5'].text1} text2={data['card5'].text2}  img = {'http://localhost:5002/getcard/'+data['card5'].image}/>,
                <CardComp key={data['card6'].id} text={data['card6'].text1}  text2={data['card6'].text2} img = {'http://localhost:5002/getcard/'+data['card6'].image}/>,
                <CardComp key={data['card7'].id} text={data['card7'].text1}  text2={data['card7'].text2} img = {'http://localhost:5002/getcard/'+data['card7'].image}/>



                ]

            );
            
            console.log(data['card1']);
          });
        } else {
          // Handle errors such as displaying an error message to the user
          console.error('Submit failed:', response.status, response.statusText);
        }
      } catch (error) {
        // Handle network errors
        console.error('Network error:', error.message);
      }
    props.setShow(false);
  }


  return (
    <>

      <Modal show={props.show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>New Card</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <InputForm setFormObj={setFormObj}/>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Add!
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default ModalPopup;