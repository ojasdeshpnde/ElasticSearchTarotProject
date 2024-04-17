import Form from 'react-bootstrap/Form';

function InputForm(props) {

  const handleChange = (e) => {
    const { name, value } = e.target;

    props.setFormObj((prevData) => ({
      ...prevData,
      [name]: sanitize(value),
    }));
  };

  function sanitize(string) {
    const map = {
        '&': ' ',
        '<': ' ',
        '>': ' ',
        '"': ' ',
        "/": ' ',
        "?": ' '
    };
    const reg = /[&<>"'/]/ig;

    return string.replace(reg, (match)=>(map[match]));
  }

  return (
    <Form>
      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Tell us about your day</Form.Label>
        <Form.Control as="textarea" name="linkText" rows={2} onChange={e => handleChange(e)} />
      </Form.Group>
    </Form>
  );
}

export default InputForm;