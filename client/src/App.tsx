import React from 'react';
import MainBar from './components/Header'
import MainBody from './components/MainBody';
import ape from 'sony ape.jpg';
import './App.css';

function App() {

  const [displayMessage, setMessage] = React.useState("");
  React.useEffect(() => {
    const callAPI = async () => {
      const response = await fetch("http://localhost:9000/testAPI").then(res => res.text()).then(res => setMessage(res));
    };
    callAPI();
  }, []);

  return (
    <div className="App">
      {/* <header className="App-header"> */}
      <MainBar />
      <MainBody />
      <p>
        {displayMessage}
      </p>
      {/* </header> */}
    </div>
  );
}

export default App;
