import logo from './logo.svg';
import {useEffect} from 'react';
import './App.css';
import getHello from './service/fetchApi';
import CardComp from './component/cardComp';

function App() {

  useEffect( () => {
    getHello();
  },[])

  return (
    <div className="App">
      <header className="App-header">
        <CardComp/>
      </header>
    </div>
  );
}

export default App;
