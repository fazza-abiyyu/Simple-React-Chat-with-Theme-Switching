from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = PyMongo()

class User:
    def __init__(self, username, password, preferences=None):
        self.username = username
        self.password = password
        self.preferences = preferences or {"theme": 0, "language": "en"}

    @classmethod
    def from_mongo(cls, mongo_user):
        return cls(
            mongo_user['username'],
            mongo_user['password'],
            mongo_user['preferences']
        )

    @staticmethod
    def create_user(username, password, preferences=None):
        hashed_password = generate_password_hash(password)
        user = {
            "username": username,
            "password": hashed_password,
            "preferences": preferences or {"theme": 0, "language": "en"}
        }
        mongo.db.users.insert_one(user)

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User.from_mongo(user_data)
        return None

    @staticmethod
    def update_preferences(username, preferences):
        mongo.db.users.update_one(
            {"username": username},
            {"$set": {"preferences": preferences}}
        )
