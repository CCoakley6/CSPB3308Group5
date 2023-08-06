import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Now you can access the environment variables using os.environ.get()
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")

    # host=db_host,
            # port=db_port,
            # dbname=db_name,
            # user=db_user,
            # password=db_password
def create_connection():
    try:
        connection = psycopg2.connect( "postgres://donutchampdb_user:KEVzKVFErrnIuUdDTtWSfJNibGJcN8Vr@dpg-cj7eof5jeehc73diu540-a/donutchampdb" ) # db link for render
#            host=db_host,
#            port=db_port,
#            dbname=db_name,
#            user=db_user,
#            password=db_password
#        )
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None