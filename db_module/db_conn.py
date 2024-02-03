import os
from sqlalchemy import create_engine, text

#Pick DB credentials from environment variables
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Create the database URL
db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

#Function to connect to the database
def db_connect():
    try:
        engine = create_engine(db_url)
        connection = engine.connect()
        # connection.close()
        return connection
    except Exception as e:
        print(e)
        return False
    
#Function to close the connection
def db_close(connection):
    try:
        connection.close()
        return True
    except Exception as e:
        return False