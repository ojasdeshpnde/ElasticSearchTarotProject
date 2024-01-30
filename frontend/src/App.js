
import {useEffect, useState} from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './component/Login';
import Signup from './component/Signup';
import Dashboard from './component/Dashboard';

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [email, setEmail] = useState("");

  useEffect( () => {
  },[])

  return (
    <main>
      <Router>
        <div className="app-container">
          <Routes>
            <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} setFname={setFname} setLname={setLname} setEmail={setEmail} isLoggedIn={isLoggedIn}/>}/>
            <Route path="/signup" element={<Signup setIsLoggedIn={setIsLoggedIn} setFname={setFname} setLname={setLname} setEmail={setEmail}  isLoggedIn={isLoggedIn}/>}/>
            <Route path="/" element={(isLoggedIn ? <Dashboard fname={fname} lname={lname} email={email} setIsLoggedIn={setIsLoggedIn}/> : <Login setIsLoggedIn={setIsLoggedIn} setFname={setFname} setLname={setLname} setEmail={setEmail} />)} />
          </Routes>
        </div>
      </Router>
    </main>
  );
}

export default App;
