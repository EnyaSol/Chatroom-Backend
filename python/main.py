from flask import Flask
from flask_socketio import SocketIO, send


app = Flask(__name__)

# Encrypts responses being sent
app.config['SECRET_KEY'] = 'mysecret'

# Wraps application with socketio functionality
socketio = SocketIO(app)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    # Send a message to all clients connected to the server
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)