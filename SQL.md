You must add a file SQL_TESTING.md to your repository and provide the following for each table (at least 3 tables):

### Table Name
rooms

### Table Description
This table stores information about different rooms

### For each field of the table, provide name and short description.
- **roomID** : unique identifier for each room
- **hostName**: the owner of the room 
- **gameStatus** : Boolean indicating the game status for the specific room
- **numPlayers** : maximum number of players in the specific room

### List of tests for verifying each table
1. Test for inserting a new room:
- Description: Check if a new room can be inserted into the rooms table successfully.
- Steps:
    - Insert a new room with a unique roomID and a gameStatus value.
    - Retrieve the inserted room and verify if the data matches the inserted values.
- Expected Result: The new room should be inserted without errors, and the retrieved data should match the inserted values.

2. Test for updating the game status of a room:
- Description: Check if the game status of an existing room can be updated.
- Steps:
    - Insert a new room into the rooms table.
    - Update the gameStatus of the inserted room.
    - Retrieve the updated room and verify if the gameStatus has been changed accordingly.
- Expected Result: The game status of the room should be updated without errors.

3. Test for deleting a room:
- Description: Check if a room can be deleted from the rooms table.
- Steps:
    - Insert a new room into the rooms table.
    - Delete the inserted room using its roomID.
    - Try to retrieve the deleted room from the table.
- Expected Result: The deleted room should not be found in the table.


### Table Name
players

### Table Description
This table stores information about players in each room

### For each field of the table, provide name and short description.
- **playerID** : unique identifier for each player
- **roomID** : reference the roomID in the rooms table
- **name**: display each player's name
- **sid**: unique identifier generated by SocketIo
- **hand**: store each player's hand data
- **discard**: discarded card information
- **isHost**: Boolean indicating room host 
- **readyStatus**: check if the player is ready or not
- **token**: the number of tokens to win the game
- **isMyTurn**: Check if this is current player's turn 

### List of tests for verifying each table

1. Test for inserting a new player:
- Description: Check if a new player can be inserted into the players table successfully.
- Steps:
    - Insert a new player with a unique playerID and a valid roomID.
    - Retrieve the inserted player and verify if the data matches the inserted values.
- Expected Result: The new player should be inserted without errors, and the retrieved data should match the inserted values.

2. Test for updating a player's hand:
- Description: Check if a player's hand can be updated.
- Steps:
    - Insert a new player into the players table.
    - Update the hand of the inserted player with new data.
    - Retrieve the updated player and verify if the hand has been changed accordingly.
- Expected Result: The player's hand should be updated without errors.

3. Test for deleting a player:
- Description: Check if a player can be deleted from the players table.
- Steps:
    - Insert a new player into the players table.
    - Delete the inserted player using its playerID.
    - Try to retrieve the deleted player from the table.
- Expected Result: The deleted player should not be found in the table.


### Table Name
deck

### Table Description
This table stores card information in a deck in each room

### For each field of the table, provide name and short description.
- **roomID** : reference the roomID in the rooms table
- **cards**: JSONB representing the cards in the deck

### List of tests for verifying each table
1. Test for inserting a new deck:
- Description: Check if a new deck can be inserted into the deck table successfully.
- Steps:
    - Insert a new deck with a valid roomID.
    - Retrieve the inserted deck and verify if the data matches the inserted values.
- Expected Result: The new deck should be inserted without errors, and the retrieved data should match the inserted values.

2. Test for updating the cards in a deck:
- Description: Check if the cards in a deck can be updated.
- Steps:
    - Insert a new deck into the deck table.
    - Update the cards of the inserted deck with new data.
    - Retrieve the updated deck and verify if the cards have been changed accordingly.
- Expected Result: The cards in the deck should be updated without errors.
3. Test for deleting a deck:
- Description: Check if a deck can be deleted from the deck table.
- Steps:
    - Insert a new deck into the deck table.
    - Delete the inserted deck using its deck_id.
    - Try to retrieve the deleted deck from the table.
- Expected Result: The deleted deck should not be found in the table.

You must also provide the following (in SQL_TESTING.md)for each data access method (at least one access method for each table or query required to get the data to display):


### Table name
rooms
### Access Method: insertRoom
Description:
Inserts a new room into the rooms table.

Parameters:
- roomID: The unique identifier for the new room.
- hostName: the owner of the room 
- numPlayers: maximum number of players in the specific room

Return Values:
- None


Tests for Insert Room:

1. Test for inserting a new room:

- Description:
    - Check if a new room can be inserted into the rooms table successfully
- Pre-conditions:
    - must have valid name, maximum number of players
- Test steps:
    1. Call the insertRoom method with valid form data
    2. Query the database to retrieve the inserted room
- Expected result:
    - The new room should be inserted into the rooms table
- Status:
    - Pass
- Post-conditions:
    - A new room can be found in the rooms table and player can join in this room


### Access Method: updateGameStatus
Description:
Updates the game status for a specific room in the rooms table.

Parameters:
- roomID: The unique identifier of the room to update.
- gameStatus: The new boolean value representing the updated game status.

Return Values:
- None

Tests for Update Game Status:

1. Test for updating the game status of a room:
- Description:
    - Check if the game status of an existing room can be updated.
- Pre-conditions:
    - The unique identifier of the room and a new boolean value representing the updated game status
- Test steps:
    1. Call the updateGameStatus method with the inserted roomID and a new gameStatus
    2. Query the database to retrieve the updated room
- Expected result:
    - The game status of the room should be updated without errors
- Acutal result:
    - The game status of the room (default value: false) should be updated to true
- Status:
    - Pass
- Post-conditions:
    - Once the game status is true, it means the game has started and no one can join the room anymore

### Access Method: deleteRoom
Description:
Deletes a room from the rooms table.

Parameters:
- roomID: The unique identifier of the room to delete.

Return Values:
- None

Tests for Delete Room:

1. Test for deleting a room:
- Description:
    - Check if a room can be deleted from the rooms table
- Pre-conditions:
    - The unique identifier of the room to delete
- Test steps:
    1. Call the deleteRoom method with the roomID
    2. Query the database to retrieve the deleted room
- Expected result:
    - The deleted room should not be found in the table
- Status:
    - Pass

### Table name
players

### Access Method: insertPlayer
Description:
Inserts a new player into the players table.

Parameters:
- playerID: The unique identifier for the new player.
- roomID: The foreign key referencing the roomID in the rooms table.
- name: The player's name
- sid: The unique identifier generated by SocketIo

Return Values:
- display an error message if the room is full

Tests for Insert Player:

1. Test for inserting a new player:
- Description:
    - Check if a new player can be inserted into the players table successfully.
- Pre-conditions:
    - valid playerID, roomID, name, sid number and some default values (hand, discard, readyStatus, token, isMyTurn etc.)
- Test steps:
    1. Call the Insert Player method with valid data shown in the above
    2. Query the database to retrieve the inserted player
- Expected result:
    - The new player should be inserted without errors, and the retrieved data should match the inserted values
- Status:
    - Pass
- Post-conditions:
    - The new player information should be inserted into the player table and we can query the player information with valid roomID

### Access Method: updatePlayerInfo
Description:
Updates the hand data for a specific player in the players table.

Parameters:
- playerID : The unique identifier of the player to update
- roomID : The foreign key referencing the roomID in the rooms table
- name: display each player's name
- sid: unique identifier generated by SocketIo
- hand: store each player's hand data
- discard: discarded card information
- isHost: Boolean indicating room host 
- readyStatus: check if the player is ready or not
- token: the number of tokens to win the game
- isMyTurn: Check if this is current player's turn 

Return Values:
- None

Tests for Update Player's information:

1. Test for updating a player's information:
- Description:
    - Check if a specific player's info are updated in the players table successfully.
- Pre-conditions:
    - valid playerID, roomID and new data
- Test steps:
    - Insert a new player into the players table
    - Call the UpdatePlayerInfo method with the inserted playerID, roomID and new data:
    - Query the database to retrieve the updated player
- Expected result:
    - The player's new info should be updated without errors
- Acutal result:
    - The new player should be inserted without errors, and the retrieved data should match the inserted values
- Status:
    - Pass
- Post-conditions:
    - the game page can display new information about each player


### Access Method: deletePlayer
Description:
Deletes a player from the players table.

Parameters:
- playerID: The unique identifier of the player to delete.

Return Values:
- None

Tests for Delete Player:

1. Test for deleting a player:
- Description:
    - Check if a player can be deleted from the players table
- Pre-conditions:
    - valid playerID
- Test steps:
    - Insert a new player into the players table
    - Call the deletePlayer method with the inserted playerID
    - Query the database to retrieve the deleted player
- Expected result:
    - The deleted player should not be found in the table
- Status:
    - Pass

## Table Name
deck

### Access Method: InsertDeck
Description:
Inserts a new deck into the deck table.

Parameters:
- roomID: The foreign key referencing the roomID in the rooms table.
- cards: The JSONB data representing the cards in the deck.

Return Values:
- display an error message if the room already had one deck

Tests for Insert Deck:

1. Test for deleting a player:
- Description:
    - Check if a player can be deleted from the players table
- Pre-conditions:
    - valid roomID and cards
- Test steps:
    - Call the Insert Deck method with valid roomID and cards values
    - Query the database to retrieve the inserted deck
- Expected result:
    - The new deck should be inserted without errors, and the retrieved data should match the inserted values
- Status:
    - Pass
- Post-conditions:
    - Once the deck is created and the game has started, each player can draw a card from the deck in their own current turn
    

### Access Method: UpdateCards
Description:
Updates the cards data for a specific deck in the deck table.

Parameters:
- roomID: The foreign key referencing the roomID in the rooms table
- cards: The new JSONB data representing the updated cards in the deck.

Return Values:
- None

Tests for Update Deck Cards:

1. Test for deleting a player:
- Description:
    - Check if the cards in a deck can be updated
- Pre-conditions:
    - valid roomID and new cards data
- Test steps:
    - Call the updateCards method with valid roomID and new cards values
    - Query the database to retrieve the new updated deck
- Expected result:
    - The cards in the deck should be updated
- Status:
    - Pass
- Post-conditions:
    - Once the deck is created and the game has started, each player can draw a card from the deck in their own current turn
    

### Access Method: Delete Deck
Description:
Deletes a deck from the deck table.

Parameters:
- roomID: The foreign key referencing the roomID in the rooms table

Return Values:
- None

Tests for Delete Deck:

1. Test for deleting a deck:
- Description:
    - Check if the cards in a deck can be updated
- Pre-conditions:
    - valid roomID and new cards data
- Test steps:
    - Insert a new deck into the deck table
    - Call the deleteDeck method with the inserted roomID
    - Query the database to retrieve the deleted deck
- Expected result:
    - The deleted deck should not be found in the table
- Status:
    - Pass


# Database Design Document

### Table Name: rooms

Fields:
- roomID : unique identifier for each room
- hostName: the owner of the room 
- gameStatus : Boolean indicating the game status for the specific room
- numPlayers : maximum number of players in the specific room

Constraints:
- roomID is a unique identifier for each room, not null
- hostName should be not null
- numPlayers should be 2 - 4.

### Table Name: players

Fields:
- playerID : unique identifier for each player
- roomID : reference the roomID in the rooms table
- name: display each player's name
- sid: unique identifier generated by SocketIo
- hand: store each player's hand data
- discard: discarded card information
- isHost: Boolean indicating room host 
- readyStatus: check if the player is ready or not
- token: the number of tokens to win the game
- isMyTurn: Check if this is current player's turn 

Constraints:
- playerID is an auto-incrementing primary key, uniquely identifying each player.
- roomID is a foreign key referencing roomID in the rooms table, not null
- Each player's roomID should have a corresponding room in the rooms table.

### Table Name: deck

Fields:
- roomID : a foreign key referencing room_id in the rooms table
- cards: JSONB representing the cards in the deck

Constraints:
- roomID is a foreign key referencing roomID in the rooms table.
- Each deck's roomID should have a corresponding room in the rooms table.


### Relationships:
One room has one game deck.
Table: rooms (roomID) -> Table: deck (roomID)

One room has multiple players.
Table: rooms (roomID) -> Table: players (roomID)

### Access Functions:
- **insertRoom**: Inserts a new room into the rooms table.
- **updateGameStatus**: Updates the game status for a specific room in the rooms table.
- **deleteRoom**: Deletes a room from the rooms table.
- **insertPlayer**: Inserts a new player into the players table.
- **updatePlayerInfo**: Updates new information for a specific player in the players table
- **deletePlayer**: Deletes a player from the players table.
- **insertDeck**: Inserts a new deck into the deck table
- **updateCards**: Updates the cards data for a specific deck in the deck table
- **deleteDeck**: Deletes a deck from the deck table

### Tests:
Test Insert Room:
- Verify if a new room can be inserted into the rooms table successfully.

Test Update Game Status:
- Verify if the game status of an existing room can be updated.

Test Delete Room:
- Verify if a room can be deleted from the rooms table.

Test Insert Player:
- Verify if a new player can be inserted into the players table successfully.

Test Update Player's information:
- Verify if a player's new information can be updated.

Test Delete Player:
- Verify if a player can be deleted from the players table.

Test Insert Deck:
- Verify if a new deck can be inserted into the deck table successfully.

Test Update Deck Cards:
- Verify if the cards in a deck can be updated.

Test Delete Deck:
- Verify if a deck can be deleted from the deck table.

### Pages Accessing Database Information:
Session Page: Displays information about each room, including the number of players, host name, room ID.
Game Page: Displays information about each player, including name, their hand, their discard and ready status etc.

### Tests for Pages:
Test Session Page:
- Verify if the Room Dashboard page displays the correct information about each room.

Test Game Page:
- Verify if the Game page displays the correct information about each player, their hand, their discard and ready status etc. the corresponding room etc.
    