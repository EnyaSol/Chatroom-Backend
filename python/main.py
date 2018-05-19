from flask import Flask
from flask_socketio import SocketIO, send


app = Flask(__name__)

# Encrypts responses being sent
app.config['SECRET_KEY'] = 'mysecret'

# Wraps application with socketio functionality
socketio = SocketIO(app)
socketio.server_options(cors_allowed_origin=["http://localhost:3000",
                                             "http://127.0.0.1:5000"
                                             "https://my-chatroom-es.herokuapp.com",
                                             "https://my-chatroom-backend-es.herokuapp.com/"])
socketio.l
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    # Send a message to all clients connected to the server
    send(msg, broadcast=True)


@app.route("/")
def index():
    return "HELLO WORLD FROM PORT " + 5000

if __name__ == '__main__':
    socketio.run(app=app, port=5000)