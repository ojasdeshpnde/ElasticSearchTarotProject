import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { useEffect } from 'react';
import getTestImage from '../service/fetchApi'
import { ReactComponent as ImageMask } from "../ImageMask.svg";
// import { getBackendIP } from '../service/localhostSettings';

function CardComp(props) {
  useEffect( () => {
    getTestImage();
  },[])

  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src={props.img}  />
      <Card.Body>
        <Card.Title>{props.text}</Card.Title>
        <Card.Text>
          {props.text2}
        </Card.Text>
        <Button variant="primary">Go somewhere</Button>
      </Card.Body>
    </Card>
  );
}

export default CardComp;