import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import InputForm from './InputForm';
import { getBackendIP } from '../service/localhostSettings';
import CardComp from './cardComp';
import OverlaySVG from './OverlaySVG';
import Spinner from 'react-bootstrap/Spinner';

function ModalPopup(props) {

  const handleClose = () => props.setShow(false);
  const handleShow = () => props.setShow(true);
  

  const [load, setLoad] = useState(false);
  const [formObj, setFormObj] = useState({
    linkText:"",
    imgText:""
  });


  const handleSubmit = async () => {
    try {
        console.log("Submitting!!")
        setLoad(true);
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
          console.log(props.board)
          response.json().then(data => {
            let tmpS = ['card1','card2','card3','card4','card5','card6','card7'];
            let tmpB = [];
            for(let i = 0 ; i < 7; i++){
              console.log(data[tmpS[i]].id)
              if(data[tmpS[i]].id >= 0){
                tmpB.push(<OverlaySVG addFlag={false} key={data[tmpS[i]].id} text={data[tmpS[i]].text1} text2={data[tmpS[i]].text2} img = {'http://localhost:5002/getcard/'+data[tmpS[i]].text2}/>);
              }
            }
            props.setBoard(tmpB);
            console.log(tmpB);
          });
        } else {
          // Handle errors such as displaying an error message to the user
          console.error('Submit failed:', response.status, response.statusText);
        }
      } catch (error) {
        // Handle network errors
        console.error('Network error:', error.message);
      }
    setLoad(false);
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
          {!load ? 
          <Button variant="primary" onClick={handleSubmit}>
            Add!
          </Button> :
          <Button variant="primary" disabled>
            <Spinner
              as="span"
              animation="grow"
              size="sm"
              role="status"
              aria-hidden="true"
            />
            Loading...
          </Button>

          }

        </Modal.Footer>
      </Modal>
    </>
  );
}

export default ModalPopup;