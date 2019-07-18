from flask import Flask, render_template , request
from flask_socketio import SocketIO , send 
import threading 
import time   
import subprocess
#Ayuda estado anterior

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


if __name__ == '__main__':
    socketio.run(app)
    print(socketio)