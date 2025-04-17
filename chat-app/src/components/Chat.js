import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Chat.css";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState("light");
  const [refresh, setRefresh] = useState(false);

  const token = localStorage.getItem("access_token");

  // Fetch user preferences (theme) when component mounts or token changes
  useEffect(() => {
    fetchPreferences();
  }, [token, refresh]);

  const fetchPreferences = () => {
    if (token) {
      axios
        .get("http://localhost:5000/preferences", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          const userTheme = res.data.theme === 1 ? "dark" : "light";
          if (theme !== userTheme) {
            setTheme(userTheme);
          }
        })
        .catch((err) => console.error("Failed to fetch preferences:", err));
    }
  };

  const handleMessageChange = (e) => setMessage(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (!token) {
      setResponse("Please log in to chat.");
      setLoading(false);
      return;
    }

    try {
      const res = await axios.post(
        "http://localhost:5000/chat",
        { message },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error chatting:", error);
      setResponse("There was an error with your message.");
    } finally {
      setLoading(false);
    }
  };

  const handleThemeChange = (themeChoice) => {
    const themeValue = themeChoice === "light" ? 0 : 1;

    axios
      .put(
        "http://localhost:5000/preferences",
        { theme: themeValue, language: "en" },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then(() => {
        
        fetchPreferences();
        setRefresh((prev) => !prev);
      })
      .catch((err) => console.error("Failed to update theme:", err));
  };

  return (
    <div className={`chat-container ${theme}`} key={theme}>
      <header>
        <h1>Chat with AI</h1>
        <div className="theme-buttons">
          <button onClick={() => handleThemeChange("light")}>Light Theme</button>
          <button onClick={() => handleThemeChange("dark")}>Dark Theme</button>
        </div>
      </header>

      <main>
        <div className="chat-box">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={message}
              onChange={handleMessageChange}
              placeholder="Type your message"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Sending..." : "Send"}
            </button>
          </form>
          {response && (
            <div className="response">
              <p><strong>Bot:</strong> {response}</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Chat;
