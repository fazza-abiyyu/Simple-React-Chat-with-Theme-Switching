import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Handle input perubahan
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "username") setUsername(value);
    if (name === "password") setPassword(value);
  };

  // Handle submit login
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Kirim permintaan login ke backend Flask dengan menggunakan 'username'
      const response = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });

      // Simpan token di localStorage (atau sessionStorage)
      localStorage.setItem("access_token", response.data.access_token);

      // Callback untuk memberitahu komponen induk (App.js) bahwa login sukses
      onLoginSuccess(response.data.access_token);

      // Redirect setelah login sukses
      navigate("/chat");  // Mengarahkan ke halaman Chat setelah login sukses
    } catch (error) {
      console.error("Login failed", error);
      setError("Username atau password salah.");
    }
  };

  // Arahkan ke halaman register
  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={username}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleRegister} style={{ marginTop: "10px" }}>
        Register
      </button>
    </div>
  );
};

export default Login;
