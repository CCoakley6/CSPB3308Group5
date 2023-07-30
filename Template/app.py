from dbconnection import create_connection

# Use the database connection function from dbconnection.py
connection = create_connection()

# Check if the connection is successful
if connection is not None:
    print("Connected to the database!")
else:
    print("Failed to connect to the database.")

