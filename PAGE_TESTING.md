# Landing Page

### Page Title
Welcome to A Love Letter to the Game Love Letter

### Page Description
This is the landing page for our game, "A Love Letter to the Game Love Letter". The page is designed to provide a welcoming and informative first impression to visitors. It includes several key components:

- **Navigation Bar**: The navigation bar is located at the top of the page. It includes the game logo, links to home and other pages, a dropdown menu for additional options, and a search bar. The navigation bar is designed to be intuitive and user-friendly, allowing visitors to easily navigate the site.

- **Welcome Section**: This section includes a large, eye-catching welcome message and a "Start Game" button. The welcome message introduces the game and sets the tone for the site. The "Start Game" button is prominently displayed to encourage visitors to play the game.

- **Game Description**: This section provides a brief overview of the game. It is designed to pique visitors' interest and give them a basic understanding of the game.

- **Game Rules**: This section outlines the rules of the game. It is written in clear, simple language to ensure that visitors can easily understand how to play the game.

- **About Us Link**: This link redirects visitors to the about us page, where they can learn more about the team behind the game.

The layout and design of the page are clean and modern, with a focus on usability. The color scheme is consistent with the game's branding.

![game_mock](./Page%20Mockups/landing_mock.png)

### Parameters needed for the page
None

### Data needed to render the page
- **Game Description**: A brief description of the game. This should be written in a way that is engaging and enticing to visitors.
- **Game Rules**: A summary of the game rules. These should be written in clear, simple language to ensure that they are accessible to all visitors.

### Link destinations for the page
- **Home**: Links back to the landing page.
- **Options**: A dropdown menu with various options. The specific options will depend on the needs and preferences of the site's visitors.
- **Search**: A search bar for the site. This should be functional and easy to use.
- **Start Game**: Links to the game session page. This should be prominently displayed to encourage visitors to play the game.
- **About Us**: Links to the about us page. This should provide visitors with information about the team behind the game.

### List of tests for verifying the rendering of the page
1. **Page Load**: Verify that the page loads without any errors.
2. **Navigation Bar**: Verify that the navigation bar is displayed at the top of the page and that all links and the search bar are functional.
3. **Welcome Section**: Verify that the welcome message and start game button are displayed and that the button redirects to the game session page.
4. **Game Description and Rules**: Verify that the game description and rules are displayed and are written in clear, simple language.
5. **About Us Link**: Verify that the about us link redirects to the about us page.


# About Us Page

### Page Title
About Us

### Page Description
This page introduces the team behind the project. It contains a brief introduction about the team and individual cards for each team member. Each card initially displays the team member's name. When the mouse pointer hovers over a card, the name fades out and a description of the team member fades in.

![game_mock](./Page%20Mockups/about_mock.png)

### Parameters needed for the page
None

### Data needed to render the page
- Team member names
- Team member descriptions

### Link destinations for the page
None

### List of tests for verifying the rendering of the page
1. Check if the page loads without any errors.
2. Check if all team member cards are displayed.
3. Check if the hover effect works on all team member cards.
4. Check if the correct description is displayed for each team member when their card is hovered over.


# Create/Join Game Session Page

### Page Title
Create/Join Game Session

### Page Description
This page provides the functionality for users to either create a new game or join an existing game. It contains two forms, one for creating a new game and another for joining an existing game. The form for creating a new game has a dropdown for selecting the number of players. The form for joining an existing game has an input field for entering the game code. There is also a link to view existing game sessions.

![game_mock](./Page%20Mockups/session_mock.png)

### Parameters needed for the page
None

### Data needed to render the page
- **Room_ID**: display a list of available rooms
- **Host Name**: show the host's name
- **Players** : display the number of players in the specific room

### Link destinations for the page
None

### List of tests for verifying the rendering of the page
1. Check if the page loads without any errors.
2. Check if both forms are displayed.
3. Check if the dropdown in the "Create a New Game" form correctly displays the options for the number of players.
4. Check if the input field in the "Join an Existing Game" form accepts text input.
5. Check if the "Create Game" and "Join Game" buttons submit the respective forms.


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

- **Homepage ('/')**: The player can use this link to leave the current room and return to the homepage.

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


# Error Page

### Page Title
Love Letter 404 Error Page

### Page Description
This is a custom error page that is displayed when a user navigates to a non-existent or broken link on the website. Instead of the default browser error message, the page will have a donut-themed design to maintain the website's visual identity. It will inform the user that they have reached a wrong page and provide options to navigate back to the home page or the session page.

![error_mock](./Page%20Mockups/error_mock.png)

### Parameters needed for the page:
None

### Data needed to render the page:
None

### Link destinations for the page:
- **Home page** : redirect the user to the landing page
- **Session page** : redirect the user to the session page

### List of tests for verifying the rendering of the page:
- Test the display of the custom 404 error message with the donut-themed design.
- Test if the home page link redirects the user to landing page
- Test if the session page link redirects the user to session page