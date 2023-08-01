from dbconnection import create_connection
from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
# Use the database connection function from dbconnection.py
connection = create_connection()

# Check if the connection is successful
if connection is not None:
    print("Connected to the database!")
else:
    print("Failed to connect to the database.")

cur = connection.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS ActiveSessions(RoomID int, RoomTitle varchar(255), HostName varchar(255), Players int)
    ''')
cur.execute('''
        CREATE TABLE IF NOT EXISTS PlayerRosters(RoomID int, Player1 varchar(255), Player2 varchar(255), Player3 varchar(255), Player4 varchar(255))
    ''')
cur.execute('''
        CREATE TABLE IF NOT EXISTS GameHistory(RoomID int, RoomTitle varchar(255), HostName varchar(255), Players int, Winner varchar(255))
    ''')
connection.commit()
connection.close()

print("Success")

