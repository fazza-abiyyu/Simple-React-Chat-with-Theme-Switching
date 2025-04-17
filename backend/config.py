import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Konfigurasi Flask dan MongoDB
    MONGO_URI = os.getenv("MONGO_URI")  # URL MongoDB, misalnya 'mongodb://localhost:27017/yourdbname'
    SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key untuk Flask
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Secret key untuk JWT
