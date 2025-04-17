from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.preference_routes import preference_bp
from routes.chat_routes import chat_bp
from models.user import mongo
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
CORS(app, resources={r"/login": {"origins": "http://localhost:3000"}})
app.config.from_object(Config)

# Inisialisasi MongoDB dan JWT
mongo.init_app(app)
jwt = JWTManager(app)

# Register blueprint untuk routes
app.register_blueprint(auth_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
