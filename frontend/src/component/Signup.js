// src/components/Signup.js
import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import './auth.css'; // Import the shared styling
import '../service/AuthService';
import { useNavigate } from 'react-router-dom';
import {loginUser, checkUserLogin} from '../service/AuthService';
import { getBackendIP } from '../service/localhostSettings';

const Signup = (props) => {

    const navigate = useNavigate();

    useEffect(() => {
        if(checkUserLogin(props.setIsLoggedIn, props.setFname, props.setLname, props.setEmail)){
            navigate('/');
        }
    },[props.isLoggedIn,navigate, props.setFname, props.setLname, props.setEmail, props.setIsLoggedIn])
 

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        fname:'',
        lname:'',
      });

      const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };



      const handleSignup = async () => {
        try {

          const response = await fetch(getBackendIP() + '/signup', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
          });

    
          if (response.ok) {
            const data = await response.json();
            // Handle the successful login, such as storing a token in local storage, redirecting, etc.
            //console.log('Signup successful:', data);
            loginUser(props.setIsLoggedIn,props.setFname,props.setLname,props.setEmail,data);
          } else {
            // Handle errors, such as displaying an error message to the user
            console.error('Singup failed:', response.status, response.statusText);
          }
        } catch (error) {
          // Handle network errors
          console.error('Network error:', error.message);
        }
      };





  return (
    <div style={{position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)'}} className="auth-container">
      <div className="auth-card">
        <h2>Sign Up</h2>
        <form>
          <div className="form-group">
            <label>First Name:</label>
            <input type="fname" id="fname" name="fname" value={formData.fname} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Last Name:</label>
            <input type="lname" id="lname" name="lname" value={formData.lname} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required />
          </div>
          <button onClick={handleSignup} >Sign Up</button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
