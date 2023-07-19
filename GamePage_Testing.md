# Game Page

### Page Title

Game Room - ROOM_ID

### Page Description

The page is a multiplayer card game page where players can join a specific room and play a card game together in real-time. The game allows multiple players to interact with each other, play cards, and track their readiness for the game. Players can see the list of participants in the room, and the game starts when the host decides to start it. There are three different layouts generated based on the number of players participating in the room. The layout consists of four player positions: South, North, West, and East, each having a hand of cards and a discard pile.

![game_mock](./Page%20Mockups/game_mock.png)

### Parameters needed for the page

- **ROOM_ID**: Unique identifier for the room where players will join and play the game.

### Data needed to render the page

1. Player Information:
    - **Name**: name of the player.
    - **Room_ID**: Unique identifier for the room where the player is in.
    - **Host Status**: A boolean indicating if the player is the host of the room

2. Game Data:
    - **List of Players**: Each player's name and readiness status (Ready or Not Ready).
    - **Cards in Hand**: The player's current hand of cards.
    - **Cards in Discard Pile**: The player's discard pile.

### Link destinations for the page

- Homepage ('/'): The player can use this link to leave the current room and return to the homepage.

### List of tests for verifying the rendering of the page

1. Test player name and room ID rendering:
- Set `name` to "David" and `room_id` to "3308".
- Verify that "Game Room - 3308" is displayed as the page title.
- Verify that the player's name "David" is displayed in the player list.

2. Test host and non-host rendering:

- Set `isHost` to true for the current player and verify that the "Start Game" and "Leave Room" buttons are displayed.
- Set `isHost` to false for another player in the room, verify that the "Ready" and "Leave Room" buttons are displayed, and test toggle ready status.

3. Test player list rendering:

- Set a list of players with their names and readiness status.
- Verify that the player list displays each player's name and readiness status correctly.

4. Test game layout rendering:

- Verify that the `room_container` is initially displayed, and the `game_container` is hidden.
- Verify that the `game_container` is now displayed, and the `room_container` is hidden when the host clicks start button.

5. Test card rendering:

- Set the data for players with their cards in hand and discard pile.
- Verify that the cards in hand and discard pile are correctly displayed for each player's position.

6. Test card interactions:

- Verify that the current player clicks the deck and draws a card when it is their turn.
- Verify that the card is moved from the player's hand to their discard pile when playing a card.

