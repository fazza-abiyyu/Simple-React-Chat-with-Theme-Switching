import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Konfigurasi Flask dan MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
