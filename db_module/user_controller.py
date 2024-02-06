from . import db_conn
from models.user import User, Base
from sqlalchemy.orm import sessionmaker
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


def create_user(email, first_name, last_name, password):
    engine = db_conn.db_engine()
    status_code = None
    message = None

    if engine:
        try:
            Session = sessionmaker(bind=db_conn.db_engine())
            session = Session()
            new_user = User(username=email, first_name=first_name, last_name=last_name, password=password)
            session.add(new_user)
            session.commit()
            session.close()
            status_code = 200
            message = "User Created"
        except IntegrityError:
            status_code = 400
            message = "User already exists"
        except Exception as e:   
            status_code = 500   
            message = str(e)
        return {"status_code": status_code, "message": message}
    else:
        return {"status_code": 500, "message": "Internal Server Error"}

def get_user_details(username):
    engine = db_conn.db_engine()
    if engine:
        Session = sessionmaker(bind=db_conn.db_engine())
        session = Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            session.close()
            return user
        except Exception as e:  
            return None
    else:
        return False
        

def get_hashed_password(username):
    return get_user_details(username).password



#test code    
# create_user("jackie@benrandis.com", "jackie", "vernor", "password1234")
# print(get_hashed_password("password.com"))