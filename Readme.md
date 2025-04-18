
# Project Overview

This project is a web-based application with a **Flask backend**, **React frontend**, and **MongoDB** as the database. The application allows users to register, log in using JWT authentication, and interact with a chatbot. The chatbot is powered by the **Gemini AI API**, and users can change their theme preference (light or dark) via chat commands.

### **Architecture**

1. **Frontend (React):**  
   The frontend is built using React, providing an interactive interface where users can register, log in, and interact with the chatbot.

2. **Backend (Flask):**  
   The backend is built with Flask, handling user authentication (JWT-based), chat interactions (via Gemini AI), and managing user preferences.

3. **Database (MongoDB):**  
   MongoDB is used to store user information and preferences (light or dark theme).

4. **Gemini AI API:**  
   The chatbot's AI functionality is powered by the Gemini AI API, which processes user inputs and responds with relevant data.

---

### **Tech Stack**
- **Frontend:** React
- **Backend:** Flask
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Token)
- **AI API:** Gemini AI

---

### **Backend Setup (Flask)**

Follow these steps to set up the backend locally:

1. **Clone the repository:**
   ```bash
   git clone [your-repository-url]
   cd [project-directory]
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   Set up the environment variables for MongoDB, JWT secret, and Gemini AI API key. Add them to a `.env` file.

   Example:
   ```
    MONGO_URI="database_url"
    SECRET_KEY="secret_key"
    JWT_SECRET_KEY="jwt_screet_key"
   ```

5. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The backend should now be running at `http://localhost:5000`.

---

### **Frontend Setup (React)**

Follow these steps to set up the frontend locally:

1. **Navigate to the frontend directory:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the React development server:**
   ```bash
   npm start
   ```

   The frontend should now be running at `http://localhost:3000`.

---

### **Backend API Endpoints**

The backend exposes 4 main endpoints:

1. **`POST /register`**  
   - Registers a new user.
   - Request body should include `username` and `password`.

2. **`POST /login`**  
   - Logs the user in and returns a JWT token.
   - Request body should include `username` and `password`.

3. **`POST /chat`**  
   - Sends a chat message to the Gemini AI API and returns the AI's response.
   - Authorization is handled via Bearer JWT in the header.
   - This endpoint also checks if the user requests a theme change and calls the `POST /preferences` endpoint to update the theme.

4. **`POST /preferences`**  
   Updates the user's preferences, including:

   - theme: theme mode (0 = light, 1 = dark)

   - language: preferred language (e.g., "en", "id")

   - notifications: notification status (true or false)
   The preferences are stored in the database and are accessible during chat interactions.
---

### **How to Test the Preferences Feature**

1. **Register and Login:**
   - First, use the `POST /register` endpoint to create a new user. Then log in with the `POST /login` endpoint to get the JWT token.

2. **Interact with the Chatbot:**
   - Once logged in, send a message using the `POST /chat` endpoint. Include the JWT token in the `Authorization` header as a Bearer token.
   - Example of chat interaction:
     ```bash
     curl -X POST http://localhost:5000/chat        -H "Authorization: Bearer YOUR_JWT_TOKEN"        -d '{"message": "What is the weather like?"}'
     ```

3. **Trigger Theme Change:**
   - In the chat, issue commands like:
     - `"light"` or `"terang"` to set the theme to light (0).
     - `"dark"` or `"gelap"` to set the theme to dark (1).
   - When a theme change is requested, the backend will call the `POST /preferences` endpoint to update the theme in the database.

4. **Reload the Page:**
   - After changing the theme, the user needs to manually reload the page to see the theme update, as the change is stored in the database and should be reflected on the next page load.

---

### **Assumptions or Simplifications Made**

- **JWT Authentication:** The authentication system uses JWT for user login and subsequent API requests. The token is used as a Bearer token in the Authorization header.
  
- **Theme Change Logic:** The chatbot listens for keywords like `"light"`, `"terang"`, `"dark"`, and `"gelap"` to trigger the theme change. This is a simple approach to ensure functionality within the project’s scope and time constraints.

- **Simplified Chatbot Interface:** Due to time limitations and the newness of integrating with the frontend, the chatbot interface is kept simple. It only handles text input and theme preference changes, without advanced interactions or error handling for edge cases.

---