# plugin.py
# import this into flask app
############################
# hold additional functions 

from dbconnection import create_connection
from flask import Flask
import psycopg2
import os
from dotenv import load_dotenv


def make_roomID(HostName):
    '''take the entered hostname as input and construct short
    noncryptographic hash code to be used to find room'''
        roomID = 33
    if len(HostName) < 5:
        HostName *= 3
    for char in HostName:
        roomID = ((( roomID << 5) + roomID) + ord(char)) & 0xFFFFF
    return str(hex(roomID))[2:]
