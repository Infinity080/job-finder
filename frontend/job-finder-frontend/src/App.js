import './App.css';
import WebsiteHeader from './Header';
import Home from './Home';
import FindJobs from './FindJobs';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <Router>
      <div className="App">
        <WebsiteHeader /> 
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/find-jobs" element={<FindJobs />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
