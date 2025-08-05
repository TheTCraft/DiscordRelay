from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a secure random key
CORS(app)

USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'

# Load preset users from users.json
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save messages to file
def save_messages(messages):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

# Load messages from file
def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r') as f:
        return json.load(f)

# Simple login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', username=session['username'])

# API to get recent messages
@app.route('/api/get_messages', methods=['GET'])
def get_messages():
    messages = load_messages()
    return jsonify(messages)

# API to send a new message (from website chat or bot)
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    username = data.get('username')
    content = data.get('content')

    if not username or not content:
        return jsonify({'error': 'Missing username or content'}), 400

    messages = load_messages()
    messages.append({'username': username, 'content': content})
    # Keep last 100 messages max
    messages = messages[-100:]
    save_messages(messages)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)