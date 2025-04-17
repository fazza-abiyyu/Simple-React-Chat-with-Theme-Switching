import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Chat.css";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState("light");

  const token = localStorage.getItem("access_token");

  // Fetch theme preference + auto-AI greeting on mount
  useEffect(() => {
    if (token) {
      axios
        .get("http://localhost:5000/preferences", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          const userTheme = res.data.theme === 1 ? "dark" : "light";
          setTheme(userTheme); // Set theme based on the fetched data
        })
        .catch((err) => console.error("Failed to fetch preferences:", err));

      // Auto initial greeting
      axios
        .post(
          "http://localhost:5000/chat",
          { message: "Hello!" },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then((res) => {
          setResponse(res.data.response);
        })
        .catch((error) => {
          console.error("Error chatting:", error);
          setResponse("There was an error fetching initial response.");
        });
    } else {
      setResponse("Please log in to start chatting.");
    }
  }, [token]);

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
      setMessage("");
    } catch (error) {
      console.error("Error chatting:", error);
      setResponse("There was an error with your message.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-container ${theme}`}>
      <header>
        <h1>Chat with AI</h1>
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
