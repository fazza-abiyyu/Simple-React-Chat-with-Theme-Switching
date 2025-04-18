import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Chat from "./components/Chat";

function App() {
  const [accessToken, setAccessToken] = useState(localStorage.getItem("access_token") || null);


  const handleLoginSuccess = (token) => {
    setAccessToken(token);
    localStorage.setItem("access_token", token);
  };


  const handleRegisterSuccess = (token) => {
    setAccessToken(token);
    localStorage.setItem("access_token", token);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login onLoginSuccess={handleLoginSuccess} />} />
          <Route path="/register" element={<Register onRegisterSuccess={handleRegisterSuccess} />} />
          <Route path="/chat" element={accessToken ? <Chat accessToken={accessToken} /> : <Login onLoginSuccess={handleLoginSuccess} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
