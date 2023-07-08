from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

rooms = {}

def create_deck():
    deck = []
    for card in cards:
        number = card['number']
        while number != 0:
            deck.append(card)
            number -= 1
    random.shuffle(deck)
    return deck

cards = [
    {
        "name": 'Plain',
        "value": 1,
        "number": 5,
        "ability": "Name a non-zero card and choose another player. If that player has that card, he or she is out of the round."
    },
    {
        "name": "Powdered",
        "value": 2,
        "number": 2,
        "ability": "Look at another player's hand.",
    },
    {
        "name": "Chocolate Sprinkle",
        "value": 3,
        "number": 2,
        "ability": "You and another player secretly compare hands. The player with the lower value is out of the round.",
    },
    {
        "name": "Bear Claw",
        "value": 7,
        "number": 1,
        "ability": "If you have this card and the 5 card or 6 card in your hand, you must discard this card.",
    },
    {
        "name": "Cinnamon Bun",
        "value": 4,
        "number": 2,
        "ability": "Until your next turn, ignore all effects from other players' cards.",
    },
    {
        "name": "Boston Cream",
        "value": 6,
        "number": 1,
        "ability": "Trade hands with another player of your choice.",
    },
    {
        "name": "Jelly Filled",
        "value": 5,
        "number": 2,
        "ability": "Choose any player (including yourself) to discard his or her hand and draw a new card.",
    },
    {
        "name": "Apple Fritter",
        "value": 8,
        "number": 1,
        "ability": "If you discard this card, you are out of the round.",
    }
]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form['name']
        room_id = request.form['room_id']
        action = request.form['action']

        session['userInfo'] = {
            "name": player_name,
            "room_id": room_id
        }

        if action == 'join':
            session['userInfo']['is_host'] = False
        elif action == 'create':
            session['userInfo']['is_host'] = True

        return redirect(f'/room/{room_id}')

    return render_template('index.html')


@app.route('/room/<room_id>')
def room(room_id):
    player_name = session.get("userInfo").get("name")
    is_host = session.get("userInfo").get("is_host")

    if not player_name:
        return redirect('/')

    return render_template('room.html', room_id=room_id, name = player_name, is_host=is_host)

@socketio.on('join')
def on_join(data):
    player_name = data['name']
    room_id = data['room_id']

    join_room(room_id)

    if room_id not in rooms:
        rooms[room_id] = {'players': [], 'status': False}

    players = rooms[room_id]["players"]

    player = {
        'sid': request.sid,
        'name': player_name,
        'room_id': room_id,
        'ready': True if session.get("userInfo").get("is_host") else False,
        'hand': [],
        'discard': [],
        'token': 0,
        'isMyTurn': False
    }

    players.append(player)

    emit('playerJoined', {'name': player_name}, room=room_id)
    emit('updatePlayerList', {'players': players}, room = room_id)


@socketio.on('ready')
def on_ready(data):
    player_name = data['name']
    room_id = data['room_id']
    ready = data["ready"]

    players = rooms[room_id]["players"]
    player = next((p for p in players if p['name'] == player_name), None)

    if player is not None:
        player['ready'] = ready
       
    emit('updatePlayerList', {'players': players}, room=room_id)  

@socketio.on('startGame')
def on_start_game(data):
    room_id = data["room_id"]
    players = rooms[room_id]['players']

    all_ready = all(p['ready'] for p in players)
    if len(players) < 2:
        emit('message', {'message': 'Not Enough Players!'}, room = room_id)
    elif all_ready == False:
        emit('message', {'message': 'Not All Players Are Ready!'}, room = room_id)
    else:
        deck = create_deck()
        for player in players:
             player['hand'].append(deck.pop())
        rooms[room_id]['deck'] = deck
        emit("game_start", {"players": rooms[room_id]['players']}, room = room_id)
        if len(deck) > 0 and len(players) > 1:
            index = random.randint(0, len(players) - 1)
            current_player = players[index]
            current_player['isMyTurn'] = True
            print(current_player)
        emit("start_round", {"player": current_player}, room = room_id)

@socketio.on('drawCard')
def draw_card(data):
    # does not work
    current_player = data["player"]
    room_id = data["room_id"]
    players = rooms[room_id]["players"]
    deck = rooms[room_id]["deck"]
    idx = 0
    for i, player in enumerate(players):
        if player.get('sid') == current_player["sid"]:
            index = i
            break
    if len(deck) > 1:
        players[idx]["hand"].append(deck.pop())
    rooms[room_id]["deck"] = deck
    emit('updateGameStatus', {"players": players}, room = room_id)


@socketio.on('leave')
def on_leave(data):
    room_id = data["room_id"]
    leave_room(room_id)

    players = rooms[room_id]["players"]
    player = next((p for p in players if p['sid'] == request.sid), None)
   
    emit('playerLeft', {'name': player['name']}, room = room_id)
    del player
    emit('updatePlayerList', {'players': rooms[room_id]["players"]}, room=room_id)  

if __name__ == '__main__':
    socketio.run(app)
