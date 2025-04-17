from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import requests
import re

# === Konfigurasi API Gemini ===
API_KEY = 'AIzaSyBKAsNdsA9PLCQYwerlPzZKEpgwRyLNUyw'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

# === Blueprint untuk Chat ===
chat_bp = Blueprint('chat', __name__)

# === Fungsi untuk dapatkan respon dari Gemini ===
def get_ai_response(message):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": message
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Request error: {e}")
        return "Terjadi kesalahan saat menghubungi layanan AI."

    except (KeyError, IndexError) as e:
        current_app.logger.error(f"Parsing error: {e}")
        return "Gagal memahami respons dari layanan AI."

# === Fungsi untuk mendapatkan deskripsi agent ===
def get_agent_description():
    return (
        "Saya beranama Zuha adalah sebuah agen virtual yang dapat membantu Anda dengan berbagai kebutuhan."
    )

def detect_theme_intent(message):
    message = message.lower()

    # Pola umum untuk perubahan tema terang
    patterns_light = [
        r'\b(mode|tema|tampilan)\s+(terang|light)\b',
        r'\bganti\s+(ke\s+)?(terang|light)\b',
        r'\b(terang|light)\b.*(dong|ya|pls|tolong)?',
        r'\baktifkan\s+(mode\s+)?terang\b',
        r'\bsuka\s+(tema\s+)?terang\b',
    ]

    # Pola umum untuk perubahan tema gelap
    patterns_dark = [
        r'\b(mode|tema|tampilan)\s+(gelap|dark)\b',
        r'\bganti\s+(ke\s+)?(gelap|dark)\b',
        r'\b(gelap|dark)\b.*(dong|ya|pls|tolong)?',
        r'\baktifkan\s+(mode\s+)?gelap\b',
        r'\bsuka\s+(tema\s+)?gelap\b',
    ]

    for pattern in patterns_light:
        if re.search(pattern, message):
            return 'light'

    for pattern in patterns_dark:
        if re.search(pattern, message):
            return 'dark'

    return None


# === Endpoint untuk mengakses AI Chat ===
@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({"error": "Pesan tidak boleh kosong."}), 400

    message_lower = message.lower()

    # Cek jika pesan kenalan
    if re.search(r'\b(kenalan|siapa\s+kamu)\b', message_lower):
        response = get_agent_description()

    # Cek intent untuk mengubah tema
    else:
        theme_intent = detect_theme_intent(message_lower)
        if theme_intent == 'light':
            response = update_user_preference(theme=0)
        elif theme_intent == 'dark':
            response = update_user_preference(theme=1)
        else:
            response = get_ai_response(message)

    return jsonify({"response": response})


# Definisikan URL untuk preferences
PREFERENCES_URL = "http://localhost:5000/preferences"

# Fungsi untuk mengirimkan permintaan ke API untuk memperbarui preferensi
def update_user_preference(theme):
    # Anda perlu mengambil token dari request untuk mengupdate preferensi
    token = request.headers.get("Authorization").split(" ")[1]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "theme": theme,
        "language": "en"
    }

    response = requests.put(PREFERENCES_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return "Tema berhasil diperbarui!"
    else:
        return f"Gagal memperbarui tema: {response.status_code} - {response.text}"
