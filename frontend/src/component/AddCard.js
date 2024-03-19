//import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import logo from '../plus2.png';

function AddCardComp(props) {

  const updateBoard = () => {
    props.setBoardSize(props.boardSize + 1);
  }
  return (
    <Card onClick={updateBoard} style={{ width: '18rem', paddingTop:0}}>
      <Card.Img variant="top" src={logo} />
      <Card.Body>
        <Card.Title>Add a Tarot Reading</Card.Title>
      </Card.Body>
    </Card>
  );
}

export default AddCardComp;