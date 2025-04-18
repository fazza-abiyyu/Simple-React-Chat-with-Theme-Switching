from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import requests
import re
from dotenv import load_dotenv
import os

# === Load Environment Variables ===
load_dotenv()

# === Konfigurasi API Gemini ===
API_KEY = os.getenv('API_KEY')
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

# === Blueprint untuk Chat ===
chat_bp = Blueprint('chat', __name__)

# === Fungsi untuk Mendapatkan Respon dari Gemini ===
def get_ai_response(message):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Ambil jawaban dari API Gemini
        raw_response = data["candidates"][0]["content"]["parts"][0]["text"]

        # Format jawaban agar lebih rapi
        formatted_response = format_response(raw_response)

        # Tambahkan flag untuk menentukan format
        return {"response": formatted_response, "format": "html"}

    except Exception as e:
        current_app.logger.error(f"Error getting AI response: {e}")
        return {"response": "Terjadi kesalahan saat menghubungi layanan AI.", "format": "plaintext"}


# === Fungsi untuk Memformat Respon ===
def format_response(response):
    # Pisahkan paragraf berdasarkan newline
    paragraphs = response.split("\n\n")

    # Format setiap paragraf berdasarkan konten
    formatted_paragraphs = []
    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()

        # Deteksi subjudul (bold)
        if re.search(r'^\w+:', clean_paragraph):
            clean_paragraph = f"**{clean_paragraph}**"

        # Deteksi daftar (bullet points)
        elif re.search(r'^[-*]\s+', clean_paragraph):
            clean_paragraph = re.sub(r'^[-*]\s+', '- ', clean_paragraph)

        # Deteksi paragraf biasa
        else:
            clean_paragraph = clean_paragraph

        formatted_paragraphs.append(clean_paragraph)

    # Gabungkan kembali paragraf dengan pemisah
    formatted_response = "\n\n".join(formatted_paragraphs)

    # Tambahkan garis horizontal untuk memisahkan bagian
    formatted_response = formatted_response.replace("----", "---")

    return formatted_response


# === Fungsi untuk Mendapatkan Deskripsi Agent ===
def get_agent_description():
    return (
        "Saya bernama Zuha, sebuah agen virtual yang dapat membantu Anda dengan berbagai kebutuhan."
    )


# === Fungsi untuk Mendeteksi Intent ===
def detect_theme_intent(message):
    patterns_light = [
        r'\b(mode|tema|tampilan)\s+(terang|light)\b',
        r'\bganti\s+(ke\s+)?(terang|light)\b',
        r'\b(terang|light)\b.*(dong|ya|pls|tolong)?',
        r'\baktifkan\s+(mode\s+)?terang\b',
        r'\bsuka\s+(tema\s+)?terang\b',
    ]

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


def detect_language_intent(message):
    patterns_en = [
        r'\b(bahasa|ganti\s+bahasa)\s+(inggris|english|en)\b',
        r'\b(ubah|switch)\s+ke\s+(inggris|english|en)\b',
        r'\bsaya\s+ingin\s+bahasa\s+(inggris|english|en)\b',
    ]

    patterns_id = [
        r'\b(bahasa|ganti\s+bahasa)\s+(indonesia|id)\b',
        r'\b(ubah|switch)\s+ke\s+(indonesia|id)\b',
        r'\bsaya\s+ingin\s+bahasa\s+(indonesia|id)\b',
    ]

    for pattern in patterns_en:
        if re.search(pattern, message):
            return 'en'

    for pattern in patterns_id:
        if re.search(pattern, message):
            return 'id'

    return None


def detect_notification_intent(message):
    patterns_enable = [
        r'\b(aktifkan|nyalakan|hidupkan)\s+(notifikasi|notifications|notif)\b',
        r'\b(notifikasi|notifications|notif)\s+(on|aktif)\b',
    ]

    patterns_disable = [
        r'\b(matikan|nonaktifkan|disable)\s+(notifikasi|notifications|notif)\b',
        r'\b(notifikasi|notifications|notif)\s+(off|mati|nonaktif)\b',
    ]

    for pattern in patterns_enable:
        if re.search(pattern, message):
            return True

    for pattern in patterns_disable:
        if re.search(pattern, message):
            return False

    return None


# === Endpoint untuk Mengakses AI Chat ===
@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message or len(message) > 500:
        return jsonify({"error": "Pesan tidak boleh kosong atau lebih dari 500 karakter."}), 400

    message_lower = message.lower()

    # Cek jika pesan kenalan
    if re.search(r'\b(kenalan|siapa\s+kamu|who\s+are\s+you|who\s+are\s+u)\b', message_lower):
        return jsonify({
            "response": get_agent_description(),
            "theme": None,
            "language": None,
            "notifications": None
        })

    # Handle intent
    intent_result = handle_intent(message_lower)
    response_data = intent_result["response"]

    # Kembalikan respons dengan informasi tema, bahasa, dan notifikasi
    return jsonify({
        "response": response_data["response"],
        "theme": response_data.get("theme"),
        "language": response_data.get("language"),
        "notifications": response_data.get("notifications"),
        "format": response_data.get("format", "plaintext")
    })


# === URL untuk Preferences ===
PREFERENCES_URL = "http://localhost:5000/preferences"


# === Fungsi untuk Memperbarui Preferensi Pengguna ===
def update_user_preference(theme=None, language=None, notifications=None):
    token = request.headers.get("Authorization").split(" ")[1]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {}
    if theme is not None:
        payload["theme"] = theme
    if language is not None:
        payload["language"] = language
    if notifications is not None:
        payload["notifications"] = notifications

    try:
        response = requests.put(PREFERENCES_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return {
                "response": "Preferensi berhasil diperbarui!",
                "theme": "light" if theme == 0 else "dark" if theme is not None else None,
                "language": language,
                "notifications": notifications
            }
        else:
            return {
                "response": f"Gagal memperbarui preferensi: {response.status_code} - {response.text}",
                "theme": None,
                "language": None,
                "notifications": None
            }

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error updating preferences: {e}")
        return {
            "response": "Terjadi kesalahan saat memperbarui preferensi.",
            "theme": None,
            "language": None,
            "notifications": None
        }


# === Fungsi untuk Menangani Semua Intent ===
def handle_intent(message_lower):
    theme_intent = detect_theme_intent(message_lower)
    if theme_intent:
        return {
            "response": update_user_preference(
                theme=0 if theme_intent == 'light' else 1,
                language=None,
                notifications=None
            ),
            "type": "theme"
        }

    language_intent = detect_language_intent(message_lower)
    if language_intent:
        return {
            "response": update_user_preference(
                theme=None,
                language=language_intent,
                notifications=None
            ),
            "type": "language"
        }

    notification_intent = detect_notification_intent(message_lower)
    if notification_intent is not None:
        return {
            "response": update_user_preference(
                theme=None,
                language=None,
                notifications=notification_intent
            ),
            "type": "notifications"
        }

    return {
        "response": get_ai_response(message_lower),
        "type": "general"
    }