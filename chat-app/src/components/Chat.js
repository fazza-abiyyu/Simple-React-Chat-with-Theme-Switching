import React, { useState, useEffect } from "react";
import axios from "axios";
import { marked } from "marked";
import "./Chat.css";

const Chat = () => {
  // State untuk chat
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // State untuk preferensi pengguna
  const [theme, setTheme] = useState("light");
  const [language, setLanguage] = useState("en");
  const [notification, setNotification] = useState(true);

  // State untuk pop-up notifikasi
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState("");
  const [prevNotification, setPrevNotification] = useState(null);

  // Token dari localStorage
  const token = localStorage.getItem("access_token");

  /**
   * Fungsi untuk menampilkan pop-up notifikasi
   */
  const showPopup = (message) => {
    setNotificationMessage(message);
    setShowNotification(true);

    // Sembunyikan pop-up setelah 3 detik
    setTimeout(() => {
      setShowNotification(false);
    }, 3000);
  };

  /**
   * Ambil preferensi pengguna dari database saat komponen dimuat
   */
  useEffect(() => {
    if (token) {
      axios
        .get("http://localhost:5000/preferences", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          console.log("Preferences fetched:", res.data.preferences); // Debugging
          const preferences = res.data.preferences;

          // Validasi nilai notifications
          const initialNotification = preferences.notifications ?? true;

          setTheme(preferences.theme === 1 ? "dark" : "light");
          setLanguage(preferences.language || "en");
          setNotification(initialNotification); // Set notification dengan nilai valid
          setPrevNotification(initialNotification); // Inisialisasi prevNotification
          console.log("Initial notification:", initialNotification); // Debugging
        })
        .catch((err) => console.error("Failed to fetch preferences:", err));
    }
  }, [token]);

  /**
   * Fungsi untuk menangani perubahan input
   */
  const handleMessageChange = (e) => setMessage(e.target.value);

  /**
   * Fungsi untuk menangani submit pesan
   */
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

      // Simpan nilai awal notifications
      const currentNotification = notification;

      // Update theme jika ada
      if (res.data.theme) {
        const newTheme = res.data.theme === "dark" ? "dark" : "light";
        setTheme(newTheme);
      }

      // Update language jika ada
      if (res.data.language) {
        setLanguage(res.data.language);
      }

      // Update notification jika ada
      if (res.data.notifications !== undefined) {
        // Validasi nilai notifications
        const newNotification = res.data.notifications ?? true; // Gunakan true sebagai default jika null

        // Update state notification
        setNotification(newNotification);

        // Tampilkan pop-up hanya jika nilai notifications berubah
        if (prevNotification !== null && newNotification !== currentNotification) {
          const message = newNotification
            ? "Notifications are now enabled."
            : "Notifications are now disabled.";
          showPopup(message); // Tampilkan pop-up notifikasi
        }

        // Update nilai sebelumnya
        setPrevNotification(newNotification);
      }

      // Update respons AI
      const formattedResponse = marked(res.data.response); // Konversi Markdown ke HTML
      setResponse(formattedResponse);
      setMessage(""); // Kosongkan input
    } catch (error) {
      console.error("Error chatting:", error);
      setResponse("There was an error with your message.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chat-container ${theme}`}>
      {/* Header */}
      <header>
        <h1>Chat with AI</h1>
        <div className="preview">
          <p>Current Language: {language.toUpperCase()}</p>
        </div>
      </header>

      {/* Pop-up Notifikasi */}
      {showNotification && (
        <div className="notification-popup">
          <p>{notificationMessage}</p>
        </div>
      )}

      {/* Main Content */}
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
              <p><strong>Bot:</strong></p>
              <div dangerouslySetInnerHTML={{ __html: response }} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Chat;