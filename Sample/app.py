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


@app.route("/")
def index():
    content = """
    <h1>Welcome to CS 3308</h1>
    """

    return content


@app.route('/session', methods=['GET', 'POST'])
def game_session():
    if request.method == 'POST':
        playerName = request.form.get("name")
        numPlayers = request.form.get("mySelect")
        roomID = request.form.get("room-id")

        if numPlayers:
            # Fake Room ID, Will be Replaced
            print("create")
            roomID = "1234"
            session['userInfo'] = {
                "name": playerName,
                "roomID": roomID,
                "isHost": True
            }
            return redirect(f'/room/{roomID}')
        else:
            print("join....")
            session['userInfo'] = {
                "name": playerName,
                "roomID": roomID,
                "isHost": False
            }

            return redirect(f'/room/{roomID}')

    return render_template('session.html')


@app.route('/room/<roomID>')
def room(roomID):
    playerName = session.get("userInfo").get("name")
    isHost = session.get("userInfo").get("isHost")

    if not playerName:
        return redirect('/')

    return render_template('room.html', roomID=roomID, name=playerName, isHost=isHost)


@socketio.on('join')
def on_join(data):
    playerName = data['name']
    roomID = data['roomID']

    join_room(roomID)

    if roomID not in rooms:
        rooms[roomID] = {'players': [], 'gameStatus': False}

    players = rooms[roomID]["players"]

    player = {
        'sid': request.sid,
        'name': playerName,
        'roomID': roomID,
        'readyStatus': True if session.get("userInfo").get("isHost") else False,
        'hand': [],
        'discard': [],
        'token': 0,
        'isMyTurn': False
    }

    players.append(player)
    emit('playerJoined', {'name': playerName}, room=roomID)
    emit('updatePlayerList', {'players': players}, room=roomID)


@socketio.on('ready')
def on_ready(data):
    playerName = data['name']
    roomID = data['roomID']
    ready = data["readyStatus"]

    players = rooms[roomID]["players"]
    player = next((p for p in players if p['name'] == playerName), None)

    if player is not None:
        player['readyStatus'] = ready

    emit('updatePlayerList', {'players': players}, room=roomID)


@socketio.on('startGame')
def on_start_game(data):
    roomID = data["roomID"]
    players = rooms[roomID]['players']

    all_ready = all(p['readyStatus'] for p in players)
    if len(players) < 2:
        emit('message', {'message': 'Not Enough Players!'}, room=roomID)
    elif all_ready == False:
        emit('message', {
             'message': 'Not All Players Are Ready!'}, room=roomID)
    else:
        deck = create_deck()
        for player in players:
            player['hand'].append(deck.pop())
        rooms[roomID]['deck'] = deck
        emit("game_start", {
             "players": rooms[roomID]['players']}, room=roomID)
        if len(deck) > 0 and len(players) > 1:
            index = random.randint(0, len(players) - 1)
            currentPlayer = players[index]
            currentPlayer['isMyTurn'] = True
        rooms[roomID]["players"][index] = currentPlayer
        emit("start_round", {"player": currentPlayer}, room=roomID)


@socketio.on('drawCard')
def draw_card(data):
    currentPlayer = data["player"]
    roomID = data["roomID"]
    players = rooms[roomID]["players"]
    deck = rooms[roomID]["deck"]
    idx = 0
    for i, player in enumerate(players):
        print("AAAAAAAAAAAAAAAAAAAA")
        print(player)
        if player.get('sid') == currentPlayer["sid"]:
            idx = i
            break
    if len(deck) > 1:
        players[idx]["hand"].append(deck.pop())
    rooms[roomID]["deck"] = deck
    emit('updateGameStatus', {"players": players}, room=roomID)


@socketio.on('playcard')
def play_card(data):
    roomID = data["roomID"]
    playerIndex = data["playerIndex"]
    player = data["player"]
    players = rooms[roomID]["players"]
    player["isMyTurn"] = False
    rooms[roomID]["players"][playerIndex] = player
    
    nextPlayerIndex = (playerIndex + 1) % len(players)
    nextPlayer = players[nextPlayerIndex]
    nextPlayer["isMyTurn"] = True
    rooms[roomID]["players"][nextPlayerIndex] = nextPlayer
    emit("updateGameStatus", {"players": rooms[roomID]["players"]}, room=roomID)
    emit('start_round', {"player": nextPlayer}, room=roomID)


@socketio.on('leave')
def on_leave(data):
    roomID = data["roomID"]
    leave_room(roomID)

    players = rooms[roomID]["players"]
    player = next((p for p in players if p['sid'] == request.sid), None)

    emit('playerLeft', {'name': player['name']}, room=roomID)
    del player
    emit('updatePlayerList', {
         'players': rooms[roomID]["players"]}, room=roomID)


if __name__ == '__main__':
    socketio.run(app)
