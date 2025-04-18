from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user import User

auth_bp = Blueprint('auth', __name__)

# === Endpoint untuk Login ===
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_username(data["username"])

    if user and check_password_hash(user.password, data["password"]):
        # Membuat access token
        access_token = create_access_token(identity=user.username)

        # Membuat response dan mengirimkan token dalam body response
        return jsonify({
            "msg": "Login successful",
            "access_token": access_token
        }), 200

    return jsonify({"msg": "Invalid credentials"}), 401

# === Endpoint untuk Register ===
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validasi username sudah ada atau belum
    if User.find_by_username(data["username"]):
        return jsonify({"msg": "Username already exists"}), 400

    # Simpan user baru ke database
    User.create_user(data["username"], data["password"], preferences=data.get("preferences"))

    return jsonify({"msg": "User registered successfully"}), 201
