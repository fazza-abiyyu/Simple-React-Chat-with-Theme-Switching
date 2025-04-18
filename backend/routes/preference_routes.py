from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

preference_bp = Blueprint('preferences', __name__)

@preference_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    current_user = get_jwt_identity()  # Ambil username dari JWT token

    # Cari pengguna di database
    user = User.find_by_username(current_user)
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan."}), 404

    # Kembalikan preferensi pengguna
    return jsonify({
        "message": "Preferensi berhasil diambil.",
        "preferences": user.preferences
    }), 200

@preference_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    current_user = get_jwt_identity()  # Ambil username dari JWT token
    data = request.get_json()

    # Validasi input
    theme = data.get("theme", None)
    language = data.get("language", None)
    notifications = data.get("notifications", None)

    if theme is None and language is None and notifications is None:
        return jsonify({"error": "Tidak ada data preferensi yang diberikan."}), 400

    # Ambil preferensi saat ini
    user = User.find_by_username(current_user)
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan."}), 404

    # Update preferensi
    new_preferences = user.preferences.copy()
    if theme is not None:
        new_preferences["theme"] = theme
    if language is not None:
        new_preferences["language"] = language
    if notifications is not None:
        new_preferences["notifications"] = notifications

    # Simpan ke database
    User.update_preferences(current_user, new_preferences)

    return jsonify({
        "message": "Preferensi berhasil diperbarui.",
        "preferences": new_preferences
    }), 200