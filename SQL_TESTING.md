You will create a list of descriptions for tables and functions being created for the project.
You must add a file SQL_TESTING.md to your repository and provide the following for each table (at least 3 tables):

    Table Name
        ActiveSessions
        
    Table Description
        Each record of the table refers to a user created game session. This table will be viewable from the 
        'Session' page of the site. Allowing users to reference which game to try and join.
        
    For each field of the table, provide name and short description.
        RoomID
            Short code representing game session. This will be created by the web application.
        RoomTitle
            A brief description provided by the user which creates a new game session, used to help 
            other users identify where to go.
        HostName
            Name entered by user who created game session, and will be associated with 'Player1' in
            the 'PlayerRosters' table.
        Players
            Number of active players in game session. Max of four.
            
    ActiveSessions Functions
        
        Generate RoomID Value - generate a code, short and unique among the current RoomID codes.
        
        Accept Player Name as Input - user joining game is queried for a string, which becomes their name.
        
        Update Players Value for Table - When another user joins, their name is entered into the associated element
            in the table for PlayerRosters, and the Players element in ActiveSessions needs to be updated.
        
        Copy Hostname from User Input - should only be used when a new game session is being created.
        
        Accept RoomTitle as Input - queried when user makes new game session.
            
    ActiveSessions Tests
        
        Create New Game Session
            Description:
                Test session creation
            Preconditions:
                So long as the session page is available
            Test Steps:
                1. navigate to the session page
                2. enter text into the required text boxes, hostname and descriptive title
                3. 'create game' button is selected
            Expected Result:
                The user will become the host of a new game session        
            Status:
                Pass
            Postconditions:
                The user's browser navigates to an instance of the game page.
                The host name provided is assigned to the user's player name.
                A new record is added to the ActiveSessions table.
                A RoomID value has been generated on behalf of the user.
                The host name and descriptive title provided are input into the
                new table record as HostName and RoomTitle values, respectively.
                A new record is added to the PlayerRoster table, and the same 
                RoomID is used as well as the same name is used for Player1.

            
        Fail Create Game Session
            Description:
                Refuse to create a new game when fields are not filled.
            Preconditions:
                User selects to create a game, but required fields are not populated.
            Test Steps:
                1. navigate to the session page.
                2. select the 'create game' button immediately.
            Expected Result:
                The user will be denied, and informed of the needed text.
            Status:
                fail
            Postconditions:
                Text will generate within the 'create game' box to inform the user of 
                the need to include the required fields.
    
    Table Name
        PlayerRosters
        
    Table Description
        When a user enters a room id and provides a player name to join a game, it will be added to this table, 
        with the associated room id. this will be used to distinguish which user is in what player slot - 1, 2, 
        3, or 4 - and will be associated to the 'Players' total in the ActiveSessions table. A game's player 
        names are visible in a game session.
        
    For each field of the table, provide name and short description.
        RoomID
            Used here from 'ActiveSessions' table to associate a player roster, which is not to be shown on the 
            'Session' page. (This excludes player 1)
        Player1
            Set to the right of 'RoomID', this will be the element where the provided user name will go when a 
            new game is created by a user. The player who's name is shown here, will be presented as the host in
            'HostName' column of 'ActiveSessions'.
        Player2
            The first user to join an active game session after it is created by the host. When this element has a 
            name, the 'Players' element in 'ActiveSessions' will indicate "2" rather than "1".
        Player3
            Similar to 'Player2', but 'Players' will indicate "3" when this element has a name.
        Player4
            The rightmost element of a record in 'PlayerRosters'. When This element has a name, another user cannot 
            enter the game Session. 
            
            
    PlayerRosters Functions
    
        Update Player Columns - When another user joins, their name is entered into the associated element
            in the table for PlayerRosters.
        
        Update Players in ActiveSessions - should be a helper function to Update Player Columns, which alters
            the value in the ActiveSessions table. Makes use of the shared RoomID between records.
            
         
    PlayerRosters Tests
        
        Add More Players to Existing Game
            Description:
                Validate that additional users can join a game
            Preconditions:
                Session page is available, and an active game session already exists
            Test Steps:
                1. user loads the session page, which presents an active game.
                2. the RoomID and a player name are entered the required textbox of the 'join a game' box.
                3. the button to join game is selected.
            Expected Result:
                The user will be a player in the same game as the host.                
            Status:
                pass
            Postconditions:
                The user's browser navigates to the correct instance of the game page.
                The player name provided is assigned to the user's player name.
                The player name is added into the next available field in the corresponding
                record in the PlayerRosters table.


        Fail Add Player Room Full
            Description:
                Refuse to add a player to a game session with no available room.
            Preconditions:
                Session page is available, and an active game session already exists, but has four players.
            Test Steps:
                1. user loads the session page, which presents an active game.
                2. the RoomID and a player name are entered the required textbox of the 'join a game' box.
                3. the button to join game is selected.
            Expected Result:
                The user will be denied, and informed that the room cannot be entered.
            Status:
                fail
            Postconditions:
                Text will generate within the 'join a game' box to inform the user that 'This
                room cannot be entered'.
        
        
        Fail Add Player Game Started
            Description:
                Refuse to add a player to a game session which has begun play.
            Preconditions:
                Session page is available, and an active game session already exists, but has already started.
            Test Steps:
                1. user loads the session page, which presents an active game.
                2. the RoomID and a player name are entered the required textbox of the 'join a game' box.
                3. the button to join game is selected.
            Expected Result:
                The user will be denied, and informed that the room cannot be entered.
            Status:
                fail
            Postconditions:
                Text will generate within the 'join a game' box to inform the user that 'This
                room cannot be entered'.
        
                
        Fail Add Player No Information
            Description:
                Refuse to add a player to a game session without player name and RoomID.
            Preconditions:
                Session page is available, but the user never entered the required information.
            Test Steps:
                1. user loads the session page, which may or may not present an active game.
                2. the RoomID and a player name are ignored for the 'join a game' box.
                3. the button to join game is selected.
            Expected Result:
                The user will be denied, and informed that the required fields must be filled out.
            Status:
                fail
            Postconditions:
                Text will generate within the 'join a game' box to inform the user of 
                the need to include the required fields.
                
        
        Fail Add Player Not Active Room
            Description:
                Refuse to add a player to a game session when the provided RoomID is not within the 
                ActiveSessions table.
            Preconditions:
                Session page is available, but the user provided RoomID does not correspond to an active
                option.
            Test Steps:
                1. user loads the session page, which may or may not present an active game.
                2. the RoomID and a player name are populated for the 'join a game' box.
                3. the button to join game is selected.
            Expected Result:
                The user will be denied, and informed that the room cannot be entered.
            Status:
                fail
            Postconditions:
                Text will generate within the 'join a game' box to inform the user that 'This
                room cannot be entered'.
    
    
    Table Name
        GameHistory
    Table Description
        Once a winner is declared in a game, the game's session will be considered "completed". A copy of the record 
        from 'ActiveSessions' will be stored here, and will be made viewable to users from the 'Session' page of the 
        site - positioned somewhat below the table of 'ActiveSessions'. This table will allow users to observe the 
        play history of the site, and the winner of a particular game.
    For each field of the table, provide name and short description.
         RoomID
            Short code representing game session. This will be created by the web application.
        RoomTitle
            A brief description provided by the user which creates a new game session, used to help other users 
            identify where to go.
        HostName
            Name entered by user who created game session, and will be associated with 'Player1' in the 
            'PlayerRosters' table.
        Players
            Number of active players in game session. Max of four. 
        Winner
            This field will be added to the information provided by the record comming from the 'ActiveSessions'
            table. Only when a game is completed and victory is awarded will a name be presented here. Otherwise, 
            it will indicate that there was not a winner.
                        
    
    GameHistory Functions
        
        Copy ActiveSessions Record - once a game is completed, the record in ActiveSessions and the player name of 
            the winner should be used to generate a new record in GameHistory.
            
    GameHistory Tests

        Completed Game Joins History
            Description:
                A new GameHistory record is produced from a completed game
            Preconditions:
                A game with at least two players has a winner declared.
            Test Steps:
                1. two or more players creat/join a game.
                2. the game is completed, and a winner is declared by the outcome.
            Expected Result:
                A row in the GameHistory Table with correct information will be presented.
            Status:
                pass
            Postconditions:
                Viewing the session page will include a new row at the top of the printed table. 
                The values included in the new row will match what was available from ActiveSessions.
                There will also be a field for the winner of the completed game, and the value
                listed will match the provided player name from the game session.
                
                
        Fail Join History Incomplete Game
            Description:
                An active game session fails to complete, and is not added to GameHistory table.
            Preconditions:
                A game with at least one player fails to complete within a preset time limit.
            Test Steps:
                1. at least one player creates a game. 
                2. the game is not completed after several hours.
            Expected Result:
                The game will cease to be available to join, but there willl be no new history record.
            Status:
                fail
            Postconditions:
                Viewing the session page will not include the new row at the top of the printed table.
                Entering the RoomID in the 'join a game' box will result in the same denial as a not
                active room.
        
    
    
You must also provide the following (in SQL_TESTING.md)for each data access method (at least one access method for each table or query required to get the data to display):


    Methods For Data Access
    
        Name
            ActiveSessions
        Description
            Session page access to ActiveSessions will present all active games, full or with availability.
        Parameters
            
        return values
            
        List of tests for verifying each access method
        
        
        
        Name
            PlayerRosters
        Description
            Game page access to PlayerRosters to present to players mid game.
        Parameters
            
        return values
            
        List of tests for verifying each access method
        
        
        Name
            GameHistory
        Description
            Session page access to GameHistory is to show the collective history of completed games to all users.
        Parameters
            
        return values
            
        List of tests for verifying each access method

Below is an example format that has been used for describing each test. Your tests might not have information for all those fields, but you should try to specify exactly how each of the pages behaves.

           Use case name : 
                Verify login with valid user name and password
            Description:
                Test the Google login page
            Pre-conditions (what needs to be true about the system before the test can be applied):
                User has valid user name and password
            Test steps:
                1. Navigate to login page
                2. Provide valid user name
                3. Provide valid password
                4. Click login button
            Expected result:
                User should be able to login
            Actual result (when you are testing this, how can you tell it worked):
                User is navigated to dashboard with successful login
            Status (Pass/Fail, when this test was performed)
                Pass
            Notes:
                N/A
            Post-conditions (what must be true about the system when the test has completed successfully):
                User is validated with database and successfully signed into their account.
                The account session details are logged in database. 
                
This should be a document that you would hand to developers (not a homework assignment where you list the question and then the answer). It should be easy to tell what your design for the database is going to encompass.

Please make sure it answers the following questions:

    What are the tables you are going to have in the database?
    What are the fields of each table?
    What are the constraints for those table fields?

    What are the relationships between tables?

    What are the functions that will be created to access the database?

    What are the tests to make sure those access routines work?

    Which pages will need to access the database information?
    What are the tests to make sure the pages access the correct data in the database?
