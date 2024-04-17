import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function LargeModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.text}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h6>
          {props.text2}
        </h6>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}
export default LargeModal;