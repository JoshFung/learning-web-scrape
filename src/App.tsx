import MainBar from 'components/Header'
import MainBody from 'components/MainBody';
import ape from 'sony ape.jpg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <MainBar />
        <MainBody />
        <p>
          recovery takes time !
        </p>
      </header>
    </div>
  );
}

export default App;
