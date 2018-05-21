# Chat server
import os
import logging
import redis
import gevent

from flask import Flask, render_template
from flask_sockets import Sockets

REDIS_URL = OS.ENVIRON['REDIS_URL']
REDIS_CHAN = 'chats'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

import redis
import gevent

class ChatBackend(object):


    """
    Interface for registerating and updateing WebSocket clients
    """

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscirbe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """
        Register a WebSocket connection for Redis updates
        Args:
            client:

        Returns:

        """
        self.clients.append(client)


    def send(self, client, data):
        """
        Send given data to the registered client.

        Removes invalid connections automatically

        Args:
            client:
            data:

        Returns:

        """

        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """
        Listens for new messages in Redis, and sends them to clients.

        Returns:

        """

        for data in self.__iter_data():
            for client in self.client:
                gevent.spawn(self.send, client, data)


    def start(self):
        """
        Maintains Redis subscription in the background

        Returns:

        """

        gevent.spawn(self.run)



    @app.route('/')
    def hello(self):
        return render_template('index.html')

    @sockets.route('/send')
    def send_message(self, ws):
        """
        Listening for incoming chat messages, insert them into Redis
        Args:
            ws: WebSocket

        Returns:

        """

        while not ws.closed:
            gevent.sleep(0.1)
            message = ws.receive()

            if message:
                app.logger.info(u'Inserting message: {}'.format(message))
                redis.publish(REDIS_CHAN, message)


    @sockets.route('/receive')
    def receive_message(self, ws):
        """
        Sends outgoing chat messages via ChatBackend
        Args:
            ws:

        Returns:

        """

        chats.register(ws)

        while not ws.closed:
            gevent.sleep(0.1)


if __name__ == '__main__':
    chats = ChatBackend()
    chats.start()