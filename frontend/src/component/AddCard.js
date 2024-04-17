//import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import logo from '../plus2.png';
import OverlaySVG from './OverlaySVG';

function AddCardComp(props) {

  const updateBoard = () => {
    props.setFormBool(true);
  }
  return (
    <div onClick={updateBoard}>
      <OverlaySVG addFlag={true} img={logo} text={"Add a reading!"} text2={"Click here if you would like a new reading."}/>
    </div>
    // <Card onClick={updateBoard} style={{ width: '18rem', paddingTop:0}}>
    //   <Card.Img variant="top" src={logo} />
    //   <Card.Body>
    //     <Card.Title>Add a Tarot Reading</Card.Title>
    //   </Card.Body>
    // </Card>
  );
}

export default AddCardComp;