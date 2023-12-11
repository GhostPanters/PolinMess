import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected to server')

@sio.on('message')
def on_message(data):
    username = data['username']
    message = data['message']
    print(f'{username}: {message}')

if __name__ == '__main__':
    username = input('Enter your username: ')
    sio.connect('http://127.0.0.1:5000')

    while True:
        message = input('Enter your message (type "exit" to quit): ')
        if message.lower() == 'exit':
            break

        sio.emit('message', {'username': username, 'message': message})

    sio.disconnect()
