## Tables in the Database

1. ActiveSessions
2. PlayerRosters
3. GameHistory

---

### 1. ActiveSessions

**Table Description:** Each record of the table refers to a user created game session. This table will be viewable from the 'Session' page of the site, allowing users to reference which game to try and join.

**Fields:**

- `RoomID`: Short code representing game session. This will be created by the web application. This is the primary key.
- `RoomTitle`: A brief description provided by the user which creates a new game session, used to help other users identify where to go. This field cannot be null.
- `HostName`: Name entered by user who created game session, and will be associated with 'Player1' in the 'PlayerRosters' table. This field cannot be null.
- `Players`: Number of active players in game session. Max of four. This field cannot be null and must be a positive integer.

**Constraints:**

- `RoomID` must be unique.
- `RoomTitle`, `HostName`, and `Players` cannot be null.
- `Players` must be a positive integer.

**Relationships:**

- One-to-many relationship with the `PlayerRosters` table. One `ActiveSessions` record can be associated with multiple `PlayerRosters` records.

## Data Access Methods

### 1. CreateGameSession

**Description:** This method creates a new game session and adds it to the ActiveSessions table.

**Parameters:** HostName, RoomTitle

**Return Values:** RoomID of the new game session.

### 2. JoinGameSession

**Description:** This method allows a user to join an existing game session.

**Parameters:** RoomID, PlayerName

**Return Values:** Success message if the player was added to the game session, error message if the game session is full.

## Tests

### Test 1: Create New Game Session

**Description:** Test session creation

**Preconditions:** So long as the session page is available

**Test Steps:**
1. Navigate to the session page
2. Enter text into the required text boxes, hostname and descriptive title
3. 'Create game' button is selected

**Expected Result:** The user will become the host of a new game session

**Status:** Pass

**Postconditions:**
- The user's browser navigates to an instance of the game page.
- The host name provided is assigned to the user's player name.
- A new record is added to the ActiveSessions table.
- A RoomID value has been generated on behalf of the user.
- The host name and descriptive title provided are input into the new table record as HostName and RoomTitle values, respectively.
- A new record is added to the PlayerRoster table, and the same RoomID is used as well as the same name is used for Player1.

### Test 2: Fail Create Game Session

**Description:** Refuse to create a new game when fields are not filled.

**Preconditions:** User selects to create a game, but required fields are not populated.

**Test Steps:**
1. Navigate to the session page.
2. Select the 'create game' button immediately.

**Expected Result:** The user will be denied, and informed of the needed text.

**Status:** Fail

**Postconditions:** Text will generate within the 'create game' box to inform the user of the need to include the required fields.

## Pages Accessing the Database

- Session Page: This page will access the `ActiveSessions` table to display all active game sessions. It will use the `CreateGameSession` and `JoinGameSession` methods to create and join game sessions.

## Page Tests

### Test 1: Session Page Displays Correct Data

**Description:** Test that the session page displays the correct data from the `ActiveSessions` table.

**Preconditions:** The `ActiveSessions` table has at least one record.

**Test Steps:**
1. Navigate to the session page.
2. Verify that all active game sessions are displayed.

**Expected Result:** All active game sessions from the `ActiveSessions` table are displayed on the session page.

**Status:** Pass

**Postconditions:** The session page displays the correct data from the `ActiveSessions` table.

---

### 2. PlayerRosters

**Table Description:** Each record of the table refers to a player in a game session. This table will be updated when a new player joins a game session.

**Fields:**

- `RoomID`: Short code representing game session. This will be created by the web application. This is the primary key.
- `Player1`: Name of the first player in the game session. This field cannot be null.
- `Player2`: Name of the second player in the game session. This field can be null if there are less than two players.
- `Player3`: Name of the third player in the game session. This field can be null if there are less than three players.
- `Player4`: Name of the fourth player in the game session. This field can be null if there are less than four players.

**Constraints:**

- `RoomID` must be unique.
- `Player1` cannot be null.
- `Player2`, `Player3`, and `Player4` can be null.

**Relationships:**

- One-to-one relationship with the `ActiveSessions` table. One `PlayerRosters` record is associated with one `ActiveSessions` record.

## Data Access Methods

### 1. AddPlayer

**Description:** This method adds a new player to an existing game session.

**Parameters:** RoomID, PlayerName

**Return Values:** Success message if the player was added to the game session, error message if the game session is full or has already started.

## Tests

### Test 1: Add More Players to Existing Game

**Description:** Validate that additional users can join a game

**Preconditions:** Session page is available, and an active game session already exists

**Test Steps:**
1. User loads the session page, which presents an active game.
2. The RoomID and a player name are entered the required textbox of the 'join a game' box.
3. The button to join game is selected.

**Expected Result:** The user will be a player in the same game as the host.

**Status:** Pass

**Postconditions:**
- The user's browser navigates to the correct instance of the game page.
- The player name provided is assigned to the user's player name.
- The player name is added into the next available field in the corresponding record in the PlayerRosters table.

### Test 2: Fail Add Player Room Full

**Description:** Refuse to add a player to a game session with no available room.

**Preconditions:** Session page is available, and an active game session already exists, but has four players.

**Test Steps:**
1. User loads the session page, which presents an active game.
2. The RoomID and a player name are entered the required textbox of the 'join a game' box.
3. The button to join game is selected.

**Expected Result:** The user will be denied, and informed that the room cannot be entered.

**Status:** Fail

**Postconditions:** Text will generate within the 'join a game' box to inform the user that 'This room cannot be entered'.

### Test 3: Fail Add Player Game Started

**Description:** Refuse to add a player to a game session which has begun play.

**Preconditions:** Session page is available, and an active game session already exists, but has already started.

**Test Steps:**
1. User loads the session page, which presents an active game.
2. The RoomID and a player name are entered the required textbox of the 'join a game' box.
3. The button to join game is selected.

**Expected Result:** The user will be denied, and informed that the room cannot be entered.

**Status:** Fail

**Postconditions:** Text will generate within the 'join a game' box to inform the user that 'This room cannot be entered'.

### Test 4: Fail Add Player No Information

**Description:** Refuse to add a player to a game session without player name and RoomID.

**Preconditions:** Session page is available, but the user never entered the required information.

**Test Steps:**
1. User loads the session page, which may or may not present an active game.
2. The RoomID and a player name are ignored for the 'join a game' box.
3. The button to join game is selected.

**Expected Result:** The user will be denied, and informed that the required fields must be filled out.

**Status:** Fail

**Postconditions:** Text will generate within the 'join a game' box to inform the user of the need to include the required fields.

### Test 5: Fail Add Player Not Active Room

**Description:** Refuse to add a player to a game session when the provided RoomID is not within the ActiveSessions table.

**Preconditions:** Session page is available, but the user provided RoomID does not correspond to an active option.

**Test Steps:**
1. User loads the session page, which may or may not present an active game.
2. The RoomID and a player name are populated for the 'join a game' box.
3. The button to join game is selected.

**Expected Result:** The user will be denied, and informed that the room cannot be entered.

**Status:** Fail

**Postconditions:** Text will generate within the 'join a game' box to inform the user that 'This room cannot be entered'.

## Pages Accessing the Database

- Session Page: This page will access the `PlayerRosters` table to display all players in a game session. It will use the `AddPlayer` method to add players to a game session.

## Page Tests

### Test 1: Session Page Displays Correct Data

**Description:** Test that the session page displays the correct data from the `PlayerRosters` table.

**Preconditions:** The `PlayerRosters` table has at least one record.

**Test Steps:**
1. Navigate to the session page.
2. Verify that all players in a game session are displayed.

**Expected Result:** All players in a game session from the `PlayerRosters` table are displayed on the session page.

**Status:** Pass

**Postconditions:** The session page displays the correct data from the `PlayerRosters` table.

---

### 3. GameHistory

**Table Description:**
Once a winner is declared in a game, the game's session will be considered "completed". A copy of the record from 'ActiveSessions' will be stored here, and will be made viewable to users from the 'Session' page of the site - positioned somewhat below the table of 'ActiveSessions'. This table will allow users to observe the play history of the site, and the winner of a particular game.

**Fields**

- `RoomID`: Short code representing game session. This will be created by the web application.
- `RoomTitle`: A brief description provided by the user which creates a new game session, used to help other users identify where to go.
- `HostName`: Name entered by user who created game session, and will be associated with 'Player1' in the 'PlayerRosters' table.
- `Players`: Number of active players in game session. Max of four.
- `Winner`: This field will be added to the information provided by the record coming from the 'ActiveSessions' table. Only when a game is completed and victory is awarded will a name be presented here. Otherwise, it will indicate that there was not a winner.

**Functions**

- `Copy ActiveSessions Record`: Once a game is completed, the record in ActiveSessions and the player name of the winner should be used to generate a new record in GameHistory.

## Tests

### Test 1: Completed Game Joins History

**Description:** A new GameHistory record is produced from a completed game

**Preconditions:** A game with at least two players has a winner declared.

**Test Steps:**
1. Two or more players create/join a game.
2. The game is completed, and a winner is declared by the outcome.

**Expected Result:** A row in the GameHistory Table with correct information will be presented.

**Status:** Pass

**Postconditions:** Viewing the session page will include a new row at the top of the printed table. The values included in the new row will match what was available from ActiveSessions. There will also be a field for the winner of the completed game, and the value listed will match the provided player name from the game session.

### Test 2: Fail Join History Incomplete Game

**Description:** An active game session fails to complete, and is not added to GameHistory table.

**Preconditions:** A game with at least one player fails to complete within a preset time limit.

**Test Steps:**
1. At least one player creates a game.
2. The game is not completed after several hours.

**Expected Result:** The game will cease to be available to join, but there will be no new history record.

**Status:** Fail

**Postconditions:** Viewing the session page will not include the new row at the top of the printed table. Entering the RoomID in the 'join a game' box will result in the same denial as a not active room.
