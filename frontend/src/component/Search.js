import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import {useState} from 'react';
import { getBackendIP } from '../service/localhostSettings';


function SearchBar(props) {

    const [query, setQuery] = useState("");
    
    const handleSubmit = async (event) => {
        event.preventDefault(); // prevent the form from submitting
        try {
          console.log("Attempting search!")
          const response = await fetch(getBackendIP() + '/getcard', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(query),
          });

    
          if (response.ok) {
            const data = await response.blob();
            console.log(data);
            const url = URL.createObjectURL(data);
            props.setImg(url);
          } else {
            console.error('Login failed:', response.status, response.statusText);
          }
        } catch (error) {
          // Handle network errors
          console.error('Network error:', error.message);
        }
      };




  return (
    <>
      <FloatingLabel
        controlId="floatingInput"
        label="Enter the name of a card"
        className="mb-3"
      >
        <Form.Control name="text" onChange={e => setQuery(e.target.value)} type="search" placeholder="Path to Exile" />
      </FloatingLabel>
      <Button onClick={handleSubmit} variant="outline-dark">Search</Button>{' '}
      <div style={{paddingBottom:10}}>

      </div>
    </>
  );
}

export default SearchBar;