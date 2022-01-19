# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from flask import render_template, flash, Flask, redirect, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, ping_timeout = 3000)

next_client_id = 0
number_of_players = 0
hostname = "tongs-macbook-pro.local"
active_rooms = set()

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/create_room', methods = ["POST"])
def create_room():
    room_id = request.form.get('create_room_id')
    error = ""
    if room_id not in active_rooms:
        active_rooms.add(room_id)
        message = "Successfully create room " + str(room_id)
        return render_template('waiting.html', message = message)
    else:
        error = "Room id already exists!"
        return render_template("index.html", error = error)

@app.route('/join_room', methods = ['GET', 'POST'])
def join_room():
    room_id = request.form.get('join_room_id')
    if room_id in active_rooms:
        message = "Successfully join room " + str(room_id)
        return render_template("waiting.html", message = message)
    else:
        error = "Room id doesn't exist"
        return render_template("index.html", error = error)


@socketio.on('connect')
def connect():
    global next_client_id
    global number_of_players
    number_of_players += 1
    next_client_id += 1
    socketio.emit('on_connect', {'client_id':  next_client_id})
    socketio.emit('game_status', {"number_of_players": number_of_players}, broadcast = True)
    

@socketio.on("disconnect")
def disconnect():
    global number_of_players
    number_of_players -= 1
    emit("game_status", {"number_of_players": number_of_players}, broadcast = True)


if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', debug = True)
