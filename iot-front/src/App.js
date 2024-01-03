import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './components/pages/Home';
import Alarm from './components/pages/Alarm';
import Device from './components/pages/Device';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/alarm" element={<Alarm />}/>
        <Route path="/device" element={<Device />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
