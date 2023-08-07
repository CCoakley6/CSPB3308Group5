from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from dbconnection import create_connection
import random
import string
import json
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

cards = [
    {
        "name": 'Plain',
        "value": 1,
        "number": 5
    },
    {
        "name": "Powdered",
        "value": 2,
        "number": 2
    },
    {
        "name": "Chocolate Sprinkle",
        "value": 3,
        "number": 2
    },
    {
        "name": "Bear Claw",
        "value": 7,
        "number": 1
    },
    {
        "name": "Cinnamon Bun",
        "value": 4,
        "number": 2
    },
    {
        "name": "Boston Cream",
        "value": 6,
        "number": 1
    },
    {
        "name": "Jelly Filled",
        "value": 5,
        "number": 2
    },
    {
        "name": "Apple Fritter",
        "value": 8,
        "number": 1
    }
]

def createDeck():
    deck = []
    for card in cards:
        number = card['number']
        while number != 0:
            deck.append(card)
            number -= 1
    random.shuffle(deck)
    return deck

def initializeTable():
    connection = create_connection()

    if connection is not None:
        print("Connected to the database!")
        cur = connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ActiveSessions (
                RoomID VARCHAR(10) PRIMARY KEY NOT NULL,
                RoomTitle TEXT NOT NULL,
                HostName VARCHAR (40) NOT NULL,
                Players INTEGER NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS PlayerRosters (
                RoomID VARCHAR(10) NOT NULL,
                Player1 JSON,
                Player2 JSON,
                Player3 JSON,
                Player4 JSON,
                FOREIGN KEY (RoomID) REFERENCES ActiveSessions (RoomID)
            )         
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS GameHistory (
                RoomID VARCHAR(10) NOT NULL,
                RoomTitle TEXT NOT NULL,
                HostName VARCHAR (40) NOT NULL,
                Players INTEGER NOT NULL,
                Winner VARCHAR(40)
            )
        ''')

        connection.commit()
        connection.close()
    else:
        print("Failed to connect to the database.")

def generateRoomID(length = 8):
    characters = string.ascii_letters + string.digits
    room_id = ''.join(random.choice(characters) for _ in range(length))
    return room_id

def listAvailableRooms():
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM ActiveSessions')
    activeSessions = cur.fetchall()

    listAvailableRooms = []

    for i in range(len(activeSessions)):
        cur.execute('''
        SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
        ''', (activeSessions[i][0],))
        record = cur.fetchone()
        if record is not None:
            players = [item for item in record if item is not None]
            if len(players) < activeSessions[i][-1]:
                listAvailableRooms.append({
                    "roomID": activeSessions[i][0],
                    "roomTitle": activeSessions[i][1],
                    "hostName": activeSessions[i][2],
                    "numPlayers": activeSessions[i][3],
                    "activeNums": len(players)
                })

    connection.commit()
    connection.close()
    return listAvailableRooms

def listHistory():
    connection = create_connection()
    cur = connection.cursor()

    cur.execute('''
    SELECT * FROM GameHistory
    WHERE WINNER IS NOT NULL
    ''')

    listHistoryRecords = cur.fetchall()

    connection.commit()
    connection.close()
    return listHistoryRecords

def addPlayer(roomID, playerName):
    player = {
        "playerID": str(uuid.uuid4()),
        "name": playerName,
        "roomID": roomID,
        "readyStatus": False,
        "hand": [],
        "discard": [],
        "token": 0,
        "isHost": False,
        "isMyTurn": False,
        "outOfRound": False,
        "invincible": False
    }
    return player

def createGameSession(roomTitle, hostName, numPlayers):
    connection = create_connection()
    roomID = generateRoomID()
    cur = connection.cursor()

    sessionRecord = '''
        INSERT INTO ActiveSessions(RoomID, RoomTitle, HostName, Players)
        VALUES (%s, %s, %s, %s)
    '''
    data = (roomID, roomTitle, hostName, numPlayers)
    cur.execute(sessionRecord, data)

    gameHistoryRecord = '''
        INSERT INTO GameHistory(RoomID, RoomTitle, HostName, Players)
        VALUES (%s, %s, %s, %s)
    '''
    data = (roomID, roomTitle, hostName, numPlayers)
    cur.execute(gameHistoryRecord, data)

    playerRecord = '''
    INSERT INTO PlayerRosters (RoomID, Player1)
    VALUES (%s, %s)
    '''
    player = {
        "playerID": str(uuid.uuid4()),
        "name": hostName,
        "roomID": roomID,
        "readyStatus": True,
        "hand": [],
        "discard": [],
        "token": 0,
        "isHost": True,
        "isMyTurn": False,
        "outOfRound": False,
        "invincible": False,
        "gameStatus": False
    }

    data = (roomID, json.dumps(player))
    cur.execute(playerRecord, data)
    connection.commit()
    connection.close()

    return roomID

def joinGameSession(roomID, playerName):
    connection = create_connection()
    cur = connection.cursor()

    cur.execute('''
    SELECT Players FROM ActiveSessions WHERE RoomID = %s
    ''', (roomID,))
    numPlayers = cur.fetchone()[0]
    print(numPlayers)

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    record = cur.fetchone()

    if record is not None:
        players = [item for item in record if item is not None]

    if len(players) == numPlayers:
        print("asdfsdafsad")
        showAvailableRooms = listAvailableRooms()
        return render_template("sessionPage.html", message = "Sorry, The room is full!", data = showAvailableRooms)
    
    if players[0]["gameStatus"] == True:
        showAvailableRooms = listAvailableRooms()
        return render_template("sessionPage.html", message = "Sorry, The game has started!", data = showAvailableRooms)
    
    for i in range(1, numPlayers):
        if record[i] == None:
            playerRecord = '''
                UPDATE PlayerRosters
                SET {} = %s
                WHERE RoomID = %s
            '''.format("Player" + str(i + 1))
        
            player = addPlayer(roomID, playerName)

            data = (json.dumps(player), roomID)
            cur.execute(playerRecord, data)

            connection.commit()
            connection.close()
            break

    return redirect(f'/room/{roomID}')

def addGameRecord(roomID, playerName):
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
        UPDATE GameHistory
        SET Winner = %s
        WHERE RoomID = %s
    ''', (playerName, roomID))
    
    connection.commit()
    connection.close()

initializeTable()

@app.route("/")
def landingPage():
    showHistory = listHistory()
    return render_template("landingPage.html", data = showHistory)

@app.route("/aboutus")
def aboutus():
    return render_template("aboutUs.html")


@app.route('/session', methods=['GET', 'POST'])
def gameSession():
    if request.method == "POST":
        playerName = request.form.get("name")
        numPlayers = request.form.get("mySelect")
        roomID = request.form.get("room-id")
        title = request.form.get("myTitle")

        if roomID is None:
            roomID = createGameSession(title, playerName, numPlayers)
            return redirect(f'/room/{roomID}')
        else:
            return joinGameSession(roomID, playerName)
    else:
        showAvailableRooms = listAvailableRooms()
        return render_template("sessionPage.html", data = showAvailableRooms )

@app.route("/room/<roomID>")
def room(roomID):
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM ActiveSessions WHERE RoomID = %s', (roomID,))
    sessionRecord = cur.fetchone()
    (RoomID, RoomTitle, HostName, Players) = sessionRecord

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    record = cur.fetchone()
    if record is not None:
        players = [item for item in record if item is not None]
    
    if sessionRecord is None:
        return render_template('404Page.html')
    
    data = {
        "roomID": RoomID,
        "roomTitle": RoomTitle,
        "hostName": HostName,
        "numPlayers": Players,
        "activeNums": len(players),
        "playerID": players[-1]["playerID"],
        "isHost": players[-1]["isHost"]
    }
    connection.close()
    return render_template("gamePage.html", data = data)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404Page.html'), 404

@socketio.on("join")
def onJoin(data):
    roomID = data["roomID"]

    join_room(roomID)

    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    players[-1]["sid"] = request.sid
    cur.execute('''
        UPDATE PlayerRosters
        SET {} = %s
        WHERE RoomID = %s
        '''.format('Player'+ str(len(players))), (json.dumps(players[-1]), roomID))
    connection.commit()
        
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    
    connection.close()
    emit('playerJoined', {'name': players[-1]["name"]}, room=roomID)
    emit('updatePlayerList', {'players': players}, room=roomID)

@socketio.on('ready')
def onReady(data):
    playerID = data["playerID"]
    roomID = data["roomID"]
    ready = data["readyStatus"]

    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()

    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    player = next((p for p in players if p['playerID'] == playerID), None)

    if player is not None:
        index = players.index(player) + 1
        player["readyStatus"] = ready
        cur.execute('''
        UPDATE PlayerRosters
        SET {} = %s
        WHERE RoomID = %s
        '''.format('Player'+ str(index)), (json.dumps(player), roomID))
        connection.commit()

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    
    connection.close()
    emit('updatePlayerList', {'players': players}, room=roomID)

@socketio.on('startGame')
def startGame(data):
    roomID = data["roomID"]
    numPlayers = int(data["numPlayers"])
    
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]

    allReady = all(p['readyStatus'] for p in players)

    if len(players) < numPlayers:
        emit('message', {'message': 'Not Enough Players!'}, room = roomID)
    elif allReady == False:
        emit('message', {
             'message': 'Not All Players Are Ready!'}, room = roomID)
    else:
        deck = createDeck()
        for player in players:
            player['hand'].append(deck.pop())

        outOfCards = []
        if len(players) == 2:
            for i in range(3):
                outOfCards.append(deck.pop())

        players[0]["deck"] = deck
        players[0]["gameStatus"] = True

        if len(deck) > 0 and len(players) > 1:
            index = random.randint(0, len(players) - 1)
            players[index]['isMyTurn'] = True

        for i in range(len(players)):
            cur.execute('''
            UPDATE PlayerRosters
            SET {} = %s
            WHERE RoomID = %s
            '''.format('Player'+ str(i + 1)), (json.dumps(players[i]), roomID))
        connection.commit()

        cur.execute('''
        SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
        ''', (roomID,))
        playerRecord = cur.fetchone()
        if playerRecord is not None:
            players = [item for item in playerRecord if item is not None]
        
        currentPlayer = players[index]
        connection.close()
        emit("startGame", {"players":  players, "outOfCards": outOfCards}, room = roomID)
        emit("yourTurn", {"player": currentPlayer}, room = roomID)

@socketio.on("nextRound")
def nextRound(data):
    players = data["players"]
    roomID = data["roomID"]

    for i in range(len(players)):
        players[i]["hand"] = []
        players[i]["discard"] = []
        players[i]["isMyTurn"] = False
        players[i]["outOfRound"] = False
        players[i]["invincible"] = False

    deck = createDeck()
    for player in players:
        player['hand'].append(deck.pop())

    outOfCards = []
    if len(players) == 2:
        for i in range(3):
            outOfCards.append(deck.pop())

    players[0]["deck"] = deck

    if len(deck) > 0 and len(players) > 1:
        index = random.randint(0, len(players) - 1)
        players[index]['isMyTurn'] = True

    connection = create_connection()
    cur = connection.cursor()

    for i in range(len(players)):
        cur.execute('''
        UPDATE PlayerRosters
        SET {} = %s
        WHERE RoomID = %s
        '''.format('Player'+ str(i + 1)), (json.dumps(players[i]), roomID))
    connection.commit()

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    
    currentPlayer = players[index]
    connection.close()
    emit("startGame", {"players":  players, "outOfCards": outOfCards}, room = roomID)
    emit("yourTurn", {"player": currentPlayer}, room = roomID)


@socketio.on('drawCard')
def drawCard(data):
    currentPlayer = data["player"]
    roomID = data["roomID"]

    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]
    deck = players[0]["deck"]
    idx = 0
    for i, player in enumerate(players):
        if player.get('sid') == currentPlayer["sid"]:
            idx = i
            break
    if len(deck) > 0:
        players[idx]["hand"].append(deck.pop())
    players[0]["deck"] = deck
    cur.execute('''
    UPDATE PlayerRosters
    SET Player1 = %s
    WHERE RoomID = %s
    ''', (json.dumps(players[0]), roomID))

    cur.execute('''
    UPDATE PlayerRosters
    SET {} = %s
    WHERE RoomID = %s
    '''.format('Player'+ str(idx + 1)), (json.dumps(players[idx]), roomID))
    connection.commit()

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]

    connection.close()
    emit('updateGameStatus', {"players": players}, room=roomID)

@socketio.on('playcard')
def playCard(data):
    roomID = data["roomID"]
    playerIndex = data["playerIndex"]
    players = data["players"]
    
    deck = players[0]["deck"]
    for i in range(len(players)):
        if len(players[i]["hand"]) == 0 and len(deck) > 0:
            players[i]["hand"].append(deck.pop())
    players[0]["deck"] = deck

    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        newPlayers = [item for item in playerRecord if item is not None]
    players[playerIndex]["isMyTurn"] = False  

    nextPlayerIndex = (playerIndex + 1) % len(newPlayers)
    
    while (players[nextPlayerIndex]["outOfRound"]):
         nextPlayerIndex = (nextPlayerIndex + 1) % len(newPlayers)

    players[nextPlayerIndex]["isMyTurn"] = True
    if players[nextPlayerIndex]["invincible"] == True:
        players[nextPlayerIndex]["invincible"] = False

    if len(players) == 2:
        if players[0]['outOfRound'] == True:
            players[1]["token"] = players[1]["token"] + 1
        elif players[1]["outOfRound"] == True:
            players[0]["token"] = players[0]["token"] + 1

    if len(players) == 3:
        outPlayer = list(filter(lambda player: player["outOfRound"] == True, players))
        winner = list(filter(lambda player: player["outOfRound"] == False, players))
        if len(outPlayer) == 2 and len(winner) == 1:
            for i in range(len(players)):
                if players[i]["playerID"] == winner[0]["playerID"]:
                    players[i]["token"] = players[i]["token"] + 1

    if len(players) == 4:
        outPlayer = list(filter(lambda player: player["outOfRound"] == True, players))
        winner = list(filter(lambda player: player["outOfRound"] == False, players))
        if len(outPlayer) == 3 and len(winner) == 1:
            for i in range(len(players)):
                if players[i]["playerID"] == winner[0]["playerID"]:
                    players[i]["token"] = players[i]["token"] + 1

    for i in range(len(newPlayers)):
        cur.execute('''
        UPDATE PlayerRosters
        SET {} = %s
        WHERE RoomID = %s
        '''.format('Player'+ str(i + 1)), (json.dumps(players[i]), roomID))

    connection.commit()

    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]

    
    emit("updateGameStatus", {"players": players}, room=roomID)

    if len(players) == 2:
        if players[0]["token"] == 7:
            addGameRecord(roomID, players[0]["name"])
            socketio.emit("message", { "message": "Congratulations, {} Wins the Game".format(players[0]["name"])}, room = roomID)
            return
        elif players[1]["token"] == 7:
            addGameRecord(roomID, players[1]["name"])
            socketio.emit("message", { "message": "Congratulations, {} Wins the Game".format(players[1]["name"])}, room = roomID)
            return
        elif players[0]['outOfRound'] == True:
            socketio.emit("message", { "message": "Congratulations, {} Wins the Round".format(players[1]["name"]), "players": players}, room = roomID)
            return
        elif players[1]["outOfRound"] == True:
            socketio.emit("message", { "message": "Congratulations, {} Wins the Round".format(players[0]["name"]), "players": players}, room = roomID)
            return
        
    if len(players) == 3:
        winner = list(filter(lambda player: player["token"] == 5, players))
        victor = list(filter(lambda player: player["outOfRound"] == False, players))
        if len(winner) == 1:
            if winner[0]["token"] == 5:
                addGameRecord(roomID, winner[0]["name"])
                socketio.emit("message", { "message": "Congratulations, {} Wins the Game".format(winner[0]["name"])}, room = roomID)
                return
        if len(victor) == 1:
            socketio.emit("message", { "message": "Congratulations, {} Wins the Round".format(victor[0]["name"]), "players": players}, room = roomID)
            return
        
    if len(players) == 4:
        winner = list(filter(lambda player: player["token"] == 4, players))
        victor = list(filter(lambda player: player["outOfRound"] == False, players))
        if len(winner) == 1:
            if winner[0]["token"] == 4:
                addGameRecord(roomID, winner[0]["name"])
                socketio.emit("message", { "message": "Congratulations, {} Wins the Game".format(winner[0]["name"])}, room = roomID)
                return
        if len(victor) == 1:
            socketio.emit("message", { "message": "Congratulations, {} Wins the Round".format(victor[0]["name"]), "players": players}, room = roomID)
            return
    
    connection.close()
    emit('yourTurn', {"player": players[nextPlayerIndex]}, room=roomID)

@socketio.on('leave')
def onLeave(data):
    roomID = data["roomID"]
    sid = data["sid"]

    leave_room(roomID)

    leftPlayer = None
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    playerRecord = cur.fetchone()
    if playerRecord is not None:
        players = [item for item in playerRecord if item is not None]

    for i in range(len(players)):
        if players[i]["sid"] == sid:
             leftPlayer = players[i]
             cur.execute('''
                UPDATE PlayerRosters
                SET {} = %s
                WHERE RoomID = %s
                '''.format('Player'+ str(i + 1)), (None, roomID))
             connection.commit()
             break
    
    cur.execute('''
    SELECT Player1, Player2, Player3, Player4 FROM PlayerRosters WHERE RoomID = %s
    ''', (roomID,))
    newRecord = cur.fetchone()
    if playerRecord is not None:
        updatedPlayers = [item for item in newRecord if item is not None]

    if len(updatedPlayers) == 0:
        cur.execute('''
        DELETE FROM PlayerRosters
        WHERE RoomID = %s            
        ''', (roomID,))
        cur.execute('''
        DELETE FROM ActiveSessions
        WHERE RoomID = %s            
        ''', (roomID,))
        connection.commit()
    connection.close()
    emit('playerLeft', {'name': leftPlayer["name"]}, room = roomID)
    emit('updatePlayerList', {'players': updatedPlayers}, room = roomID)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)