from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from cryptography.fernet import Fernet
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

def load_or_create_fernet_key():
    env_key = os.environ.get("FERNET_KEY")
    if env_key:
        return env_key.encode()
    key_path = Path(__file__).with_name("fernet.key")
    if key_path.exists():
        return key_path.read_bytes().strip()
    new_key = Fernet.generate_key()
    try:
        key_path.write_bytes(new_key)
    except Exception:
        # If we can't write the key file, still proceed with in-memory key
        pass
    return new_key

# Persistent encryption key (env FERNET_KEY or fernet.key file)
key = load_or_create_fernet_key()
cipher = Fernet(key)

encrypted_password = None
session_active = False
current_state = "waiting"


@app.route("/")
def home():
    return render_template("dashboard.html")

# Receive state from ESP32
@app.route("/upload", methods=["POST"])
def upload_state():
    global current_state, session_active
    data = request.get_json(silent=True) or {}
    state = data.get("state")
    if state is None:
        return jsonify({"error": "Missing 'state' in JSON body"}), 400
    # If device signals session completion
    if isinstance(state, str) and state.lower() == "done":
        session_active = False
        current_state = "done"
        return jsonify({"status": "ok", "session_active": session_active})
    current_state = state
    return jsonify({"status": "ok"})


# Receive session commands from dashboard or timer
@app.route("/start_session", methods=["POST"])
def start_session():
    global session_active
    session_active = True
    return jsonify({"status": "session_started"})


@app.route("/end_session", methods=["POST"])
def end_session():
    global session_active
    session_active = False
    return jsonify({"status": "session_completed"})


# Save parent password (encrypted)
@app.route("/set_password", methods=["POST"])
def set_password():
    global encrypted_password
    data = request.get_json(silent=True) or {}
    pwd = data.get("password")
    if not pwd:
        return jsonify({"error": "Password is required"}), 400
    encrypted_password = cipher.encrypt(pwd.encode())   # store encrypted
    return jsonify({"status": "password_saved"})


# Reveal password if session is completed
@app.route("/get_password", methods=["GET"])
def get_password():
    if encrypted_password is None:
        return jsonify({"status": "no_password_set"}), 404

    if session_active:
        return jsonify({"status": "locked"}), 423  # Locked

    # decrypt password for reveal
    decrypted = cipher.decrypt(encrypted_password).decode()
    return jsonify({"status": "unlocked", "password": decrypted})


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"focus_state": current_state, "session_active": session_active})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
