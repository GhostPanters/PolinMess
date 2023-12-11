from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Имя файла для хранения сообщений
MESSAGES_FILE = 'messages.json'

# Загрузка сообщений из файла (если он существует)
try:
    with open(MESSAGES_FILE, 'r') as file:
        messages = json.load(file)
except FileNotFoundError:
    messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('connect')
def handle_connect():
    # При подключении отправим клиенту все сохраненные сообщения
    emit('all_messages', messages)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']

    # Добавление сообщения к списку
    messages.append({'username': username, 'message': message})

    # Сохранение списка сообщений в файл
    with open(MESSAGES_FILE, 'w') as file:
        json.dump(messages, file)

    emit('message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
