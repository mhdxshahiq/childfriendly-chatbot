from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from chatbot import ChildFriendlyChatbot
from voice_handler import VoiceHandler
import os
import json

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Needed for Flask session

chatbot = ChildFriendlyChatbot()
voice = VoiceHandler()

# 📁 Directory to store chat files
CHAT_DIR = "chat_logs"
os.makedirs(CHAT_DIR, exist_ok=True)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in ["student1", "student2"] and password == username:
            session["user"] = username
            return redirect(url_for('chat_page'))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/chat_page')
def chat_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Not logged in"}), 403

    # Load user's chat history
    history_file = os.path.join(CHAT_DIR, f"chat_history_{user}.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            context = json.load(f)
    else:
        context = []

    user_input = request.json.get("message", "")
    chatbot.set_context(context)
    response = chatbot.get_response(user_input)

    # Add to history
    context.append({"role": "user", "message": user_input})
    context.append({"role": "assistant", "message": response})

    with open(history_file, "w") as f:
        json.dump(context, f, indent=2)

    audio_url = voice.speak(response)
    return jsonify({"reply": response, "audio_url": audio_url})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
