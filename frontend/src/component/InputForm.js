import Form from 'react-bootstrap/Form';

function InputForm() {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Question 1</Form.Label>
        <Form.Control as="textarea" rows={2} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Question 2</Form.Label>
        <Form.Control as="textarea" rows={2} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Question 3</Form.Label>
        <Form.Control as="textarea" rows={2} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Question 4</Form.Label>
        <Form.Control as="textarea" rows={2} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Question 5</Form.Label>
        <Form.Control as="textarea" rows={2} />
      </Form.Group>
    </Form>
  );
}

export default InputForm;