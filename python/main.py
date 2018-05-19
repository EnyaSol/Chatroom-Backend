from flask import Flask, render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)

# Encrypts responses being sent
app.config['SECRET_KEY'] = 'mysecret'

list_of_cors_acceptable_sites = ["http://localhost:3000",
                                             "http://127.0.0.1:5000",
                                             "https://my-chatroom-es.herokuapp.com",
                                             "https://my-chatroom-backend-es.herokuapp.com/"]

# Wraps application with socketio functionality
socketio = SocketIO(app, cors_allowed_origins = list_of_cors_acceptable_sites)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    # Send a message to all clients connected to the server
    send(msg, broadcast=True)

@socketio.on('send_message')
def handle_source(json_data):
    text = json_data['message']
    socketio.emit('echo', {'echo': 'Server Says: ' + text})


@app.route("/")
def index():
    return render_template('test.html')

if __name__ == '__main__':
    socketio.run(app=app, port=5000)