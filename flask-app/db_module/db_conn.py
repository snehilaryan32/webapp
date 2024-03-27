import os
from sqlalchemy import create_engine, text
from models.user import User, EmailTracker, Base


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
    
#Function to create the engine
def db_engine():
    try:
        engine = create_engine(db_url)
        return engine
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
    
#Function to execute a query
def db_execute(connection, query):
    try:
        result = connection.execute(text(query))
        return result
    except Exception as e:
        return False
    
#Botstrapping Function 
def db_bootstrap():
    try:
        engine = db_engine()
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(e)
        return False



#################################################################################################################################################



# Testing Functions 
# print(db_bootstrap())
    
