Project Overview
This project is a web-based application with a Flask backend, React frontend, and MongoDB as the database. The application allows users to register, log in, and interact with a chatbot. The chatbot feature includes querying and changing themes (light/dark) via user commands, powered by the Gemini AI API.

Architecture
Frontend (React):
The frontend is built using React, providing an interactive interface where users can register, log in, and interact with the chatbot.

Backend (Flask):
The backend is built with Flask, handling user authentication, serving the chat API, and interacting with the database.

Database (MongoDB):
MongoDB is used to store user information and chat history.

Gemini AI API:
The chatbot's AI functionality is powered by the Gemini AI API, which allows the chatbot to understand and process user inputs, including commands for changing themes.

Tech Stack
Frontend: React

Backend: Flask

Database: MongoDB

AI API: Gemini AI

Setup Instructions
Follow these steps to set up both the frontend and backend locally:

Backend Setup (Flask)
Clone the repository:

bash
Copy code
git clone [your-repository-url]
cd [project-directory]
Create and activate a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set environment variables: You need to set up the environment variables for MongoDB and Gemini AI API keys. You can add them to a .env file.

Example:

ini
Copy code
MONGODB_URI=your_mongodb_uri
GEMINI_API_KEY=your_gemini_api_key
Run the Flask server:

bash
Copy code
python app.py
Backend should now be running at http://localhost:5000.

Frontend Setup (React)
Navigate to the frontend directory:

bash
Copy code
cd client
Install dependencies:

bash
Copy code
npm install
Run the React development server:

bash
Copy code
npm start
Frontend should now be running at http://localhost:3000.

How to Test the Preferences Feature
Login or Register: After starting both the frontend and backend servers, navigate to http://localhost:3000. You can register a new account or log in if you already have one.

Interact with the Chatbot: Once logged in, the user will be directed to the chatbot page. You can interact with the chatbot and issue commands like:

"Change to dark theme"

"Switch to light theme" These commands will trigger the chatbot to update the theme accordingly.

Verify Theme Change: After sending the command, check if the theme updates as expected in the frontend.

Assumptions or Simplifications Made
No Full Gemini AI Integration: If the Gemini API is not available, the chatbot functionality can be simulated with a basic mock interface in the frontend, mimicking the theme switch functionality.

Basic Authentication: The authentication system is simplified and does not include advanced features like email verification or password resets.