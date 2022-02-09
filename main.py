# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datetime import datetime
from flask import render_template, flash, Flask, redirect, request, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from game import Game
from order import Order
import globals


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, ping_timeout = 3000)

next_client_id = 0
number_of_players = 0
hostname = "tongs-macbook-pro.local"
active_rooms = set()
active_games = {}

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
        message = "Successfully created room " + str(room_id)
        return render_template('room.html', message = message)
    else:
        error = "Room id already exists!"
        return render_template("index.html", error = error)

@app.route('/join_room', methods = ['GET', 'POST'])
def join_room():
    room_id = request.form.get('join_room_id')
    if room_id in active_rooms:
        message = "Successfully joined room " + str(room_id)
        return render_template("room.html", message = message)
    else:
        error = "Room id doesn't exist"
        return render_template("index.html", error = error)


@socketio.on('connect')
def connect():
    global next_client_id
    global number_of_players
    number_of_players += 1
    next_client_id += 1
    socketio.emit('on_connect', {'client_id':  next_client_id}, broadcast = False)
    socketio.emit('game_status', {"number_of_players": number_of_players}, broadcast = True)

@socketio.on('game_start')
def game_start(msg):
    print(msg)
    players_id = [i for i in range(1,int(msg["number_of_players"])+1)] # TODO: figure out the exact player ids!
    globals.game = Game(players_id)
    socketio.emit("game_start", {})
    

@socketio.on("disconnect")
def disconnect():
    global number_of_players
    number_of_players -= 1
    emit("game_status", {"number_of_players": number_of_players}, broadcast = True)

@socketio.on("order")
def process_order(msg):
    player_id = int(msg["player_id"])
    type = msg["type"]
    side = msg["side"]
    price = float(msg["price"])
    quantity = int(msg["quantity"])

    order = Order(player_id, type, side, price, quantity, datetime.utcnow())

    if type == "buy":
        globals.game.players[player_id].buying_power -= price * quantity

    orderbook = globals.game.over_under_book
    if type == "future":
        orderbook = globals.game.future_book
    elif type == "option":
        orderbook = globals.game.option_book
    trading_price, bids, asks, transactions = orderbook.match_order(order)
    # print("trading price", trading_price)
    # print("bid list", bids)
    # print("ask list", asks)
    emit("update", {
        "type": type,
        "trading_price": trading_price,
        "bids": bids,
        "asks": asks,
        "transactions": transactions,
        "players_status": [player for player in globals.game.players]
    }, broadcast = True)


    print(player_id, type, side, price, quantity, transactions)


if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', debug = True)
