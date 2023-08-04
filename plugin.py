# plugin.py
# import this into flask app
############################
# hold additional functions 

from dbconnection import create_connection
from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv


def Initialize_Tables():
    '''intitialize the database tables.'''
    connection = create_connection()
    # Check if the connection is successful
    if connection is not None:
        print("Connected to the database!")
    else:
        print("Failed to connect to the database.")
    cur = connection.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS ActiveSessions(
                RoomID int, RoomTitle varchar(255), HostName varchar(255), Players int);
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS PlayerRosters(
                RoomID int, Player1 varchar(255), Player2 varchar(255), Player3 varchar(255), Player4 varchar(255));
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS GameHistory(
                RoomID int, RoomTitle varchar(255), HostName varchar(255), Players int, Winner varchar(255));
                ''')
    connection.commit()
    connection.close()
    print("Success")


def make_RoomID(HostName):
    '''take the entered hostname as input and construct short
    noncryptographic hash code to be used to find room'''
        RoomID = 33
    if len(HostName) < 5:
        HostName *= 3
    for char in HostName:
        RoomID = ((( RoomID << 5) + RoomID) + ord(char)) & 0xFFFFF
    return str(hex(RoomID))[2:]


def make_GameHistory(RoomID, Winner):
    '''generate and insert a new record into GameHistory table. 
    RoomID and Winner are strings, and Winner must be identical 
    to a field of PlayerRosters table, as in 'Player3'.'''
    # Use the database connection function from dbconnection.py
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
                INSERT INTO GameHistory (RoomID, RoomTitle, HostName, Players, Winner)
                SELECT ActiveSessions.*, PlayerRosters.''' +Winner+ '''
                FROM ActiveSessions
                LEFT JOIN PlayerRosters
                ON ActiveSessions.RoomID=PlayerRosters.RoomID
                WHERE RoomID=''' +RoomID+ ''';
                ''')
    connection.commit()
    connection.close()


def update_PlayerRosters(RoomID, PlayerName):
    '''update the field of players for a given session, and 
    update names within a roster.'''
    success = False
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
                SELECT Players
                FROM ActiveSessions
                WHERE RoomID=''' +RoomID+ ''';
                ''')
    
    result = cur.fetchone()
    if result != None & result[0] < 4:
        cur.execute('''
                    UPDATE ActiveSessions
                    SET Players=Players+1 
                    WHERE RoomID=''' +RoomID+ ''';
                    ''')
        if result[0] == 0:
            cur.execute('''
                        UPDATE PlayerRosters
                        SET Player1=''' +PlayerName+ ''' 
                        WHERE RoomID=''' +RoomID+ ''';
                        ''')
            success = True
        else if result[0] == 1:
            cur.execute('''
                        UPDATE PlayerRosters
                        SET Player2=''' +PlayerName+ ''' 
                        WHERE RoomID=''' +RoomID+ ''';
                        ''')
            success = True
        else if result[0] == 2:
            cur.execute('''
                        UPDATE PlayerRosters
                        SET Player3=''' +PlayerName+ ''' 
                        WHERE RoomID=''' +RoomID+ ''';
                        ''')
            success = True
        else:
            cur.execute('''
                        UPDATE PlayerRosters
                        SET Player4=''' +PlayerName+ ''' 
                        WHERE RoomID=''' +RoomID+ ''';
                        ''')
            success = True
    connection.commit()
    connection.close()
    return success


def make_ActiveSession(HostName, RoomTitle):
    '''generate a new record in ActiveSessions table. HostName 
    and Roomtitle arguments must be strings.'''
    RoomID = make_RoomID(HostName)
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
                INSERT INTO ActiveSessions (RoomID, RoomTitle, HostName, Players)
                VALUES (''' +RoomID+ ''', ''' +RoomTitle+ ''', ''' +HostName+ ''', 0 );
                ''')    
    connection.commit()
    connection.close()
    update_PlayerRosters(RoomID, HostName)


def search_RoomID(RoomID):
    '''search the ActiveSessions table and verify one with the 
    entered RoomID exists. If room does not exist, do not redirect.'''
    room_exists = False
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
                SELECT RoomID
                FROM ActiveSessions
                WHERE RoomID=''' +RoomID+ ''';
                ''')
    
    result = cur.fetchone()
    connection.close()
    if result != None & result[0] == RoomID:
        room_exists = True
    return room_exists


def check_Players(RoomID):
    '''search the ActiveSessions table and verify that the room is
    not currently full.'''
    has_room = False
    connection = create_connection()
    cur = connection.cursor()
    cur.execute('''
                SELECT Players
                FROM ActiveSessions
                WHERE RoomID=''' +RoomID+ ''';
                ''')
    
    result = cur.fetchone()
    connection.close()
    if result != None & result[0] < 4:
        has_room = True
    return has_room


