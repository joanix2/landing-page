import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Unsubscribe from "./pages/Unsubscribe";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/unsubscribe" element={<Unsubscribe />} />
      </Routes>
    </Router>
  );
}

export default App;
