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
        <Form.Label>Title</Form.Label>
        <Form.Control as="textarea" name="linkText" rows={2} onChange={e => handleChange(e)} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
        <Form.Label>Image Search</Form.Label>
        <Form.Control name="imgText" as="textarea" rows={2} onChange={e => handleChange(e)}/>
      </Form.Group>
    </Form>
  );
}

export default InputForm;