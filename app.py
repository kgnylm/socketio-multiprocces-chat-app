from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import mongoengine as me


app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = 'secret!'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chat'

socketio = SocketIO(app, cors_allowed_origins="*")

me.connect('chat', host='mongodb://localhost:27017/chat')

from routes import *
from events import *

if __name__ == '__main__':
    from workers import start_workers
    start_workers()
    socketio.run(app, debug=True)
