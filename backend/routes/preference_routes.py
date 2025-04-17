from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

preference_bp = Blueprint('preferences', __name__)

@preference_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    username = get_jwt_identity()
    user = User.find_by_username(username)

    if user:
        return jsonify(user.preferences), 200
    return jsonify({"msg": "User not found"}), 404

@preference_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    username = get_jwt_identity()
    data = request.get_json()

    user = User.find_by_username(username)
    if user:
        User.update_preferences(username, data)
        return jsonify({"msg": "Preferences updated successfully"}), 200

    return jsonify({"msg": "User not found"}), 404
