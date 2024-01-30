// src/components/Login.js
import React, { useState , useEffect} from 'react';
import { Link } from 'react-router-dom';
import './auth.css'; // Import the shared styling
import {loginUser, checkUserLogin} from '../service/AuthService';
import { useNavigate } from 'react-router-dom';
import AlertCom from './Alert'
import { getBackendIP } from '../service/localhostSettings';

const Login = (props) => { 

    const navigate = useNavigate();

    const [loginAlert, setLoginAlert] = useState(false);
    const [loginAlertText, setLoginAlertText] = useState("");
    const [loginAlertTitle, setLoginAlertTitle] = useState("");
    const [loginAlertType, setLoginAlertType] = useState("success");

    useEffect(() => {
        if(checkUserLogin(props.setIsLoggedIn, props.setFname, props.setLname, props.setEmail)){
            navigate('/');
        }
    },[props.isLoggedIn,navigate, props.setFname, props.setLname, props.setEmail, props.setIsLoggedIn])

    const [formData, setFormData] = useState({
        email: '',
        password: '',
      });

      const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
          ...prevData,
          [name]: value,
        }));
      };



      const handleLogin = async () => {
        try {
          console.log("Attempting login!")
          const response = await fetch(getBackendIP() + '/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
          });

    
          if (response.ok) {
            const data = await response.json();
            loginUser(props.setIsLoggedIn,props.setFname,props.setLname,props.setEmail,data);
          } else {
            setLoginAlert(true);
            setLoginAlertText("Wrong email and password");
            setLoginAlertTitle("Login Unsuccesful");
            setLoginAlertType("danger");
            // Handle errors such as displaying an error message to the user
            console.error('Login failed:', response.status, response.statusText);
          }
        } catch (error) {
          // Handle network errors
          console.error('Network error:', error.message);
        }
      };
      
    




  return (
    <div style={{position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)'}} className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        <form>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required />
          </div>
          <button onClick={handleLogin}>Login</button>
        </form> 
        <p>
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
        
        {loginAlert ? <AlertCom loginAlertText={loginAlertText} loginAlertTitle={loginAlertTitle} loginAlertType={loginAlertType}/> : null}

      </div>
    </div>
  );
};

export default Login;
