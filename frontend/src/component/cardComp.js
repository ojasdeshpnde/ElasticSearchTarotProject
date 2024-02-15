import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { useEffect } from 'react';
import getTestImage from '../service/fetchApi'
// import { getBackendIP } from '../service/localhostSettings';

function CardComp(props) {
  useEffect( () => {
    getTestImage();
  },[])

  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src={props.img}  />
      <Card.Body>
        <Card.Title>Card Title</Card.Title>
        <Card.Text>
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </Card.Text>
        <Button variant="primary">Go somewhere</Button>
      </Card.Body>
    </Card>
  );
}

export default CardComp;