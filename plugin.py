# plugin.py
# import this into flask app
############################
# hold additional functions 

from dbconnection import create_connection
from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv


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
                WHERE RoomID=''' +RoomID+ '''
                ''')
    connection.commit()
    connection.close()