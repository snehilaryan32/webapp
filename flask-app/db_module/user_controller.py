from . import db_conn
from models.user import User, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime


#################################################User Creation############################################
def create_user(user_details):
    engine = db_conn.db_engine()
    status_code = None
    description = None
    if engine:
        try:
            Session = sessionmaker(bind=db_conn.db_engine())
            session = Session()
            new_user = User(user_details)
            session.add(new_user)
            session.commit()
            session.close()
            status_code = 201
            # description = "User Created"
        except IntegrityError:
            status_code = 400
            description = "User already exists"
        except Exception as e:   
            status_code = 500
            description = str(e)
        return {"status_code": status_code, "description": description}
    else:
        return {"status_code": 500, "description": "Internal Server Error"}

#################################################Get User Details#########################################
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
        
#################################################Get Hashed Password#########################################
def get_hashed_password(username):
    return get_user_details(username).password

#################################################Update User Details#########################################
def update_user_details(username, updated_user_details):
    engine = db_conn.db_engine()
    status_code = None
    # message = None
    if engine:
        Session = sessionmaker(bind=db_conn.db_engine())
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        user.first_name = updated_user_details['first_name']
        user.last_name = updated_user_details['last_name']
        user.password = updated_user_details['password']
        user.account_updated = datetime.datetime.now()
        session.commit()
        session.close()
        status_code = 204
        #message = "User Updated"   
    else:
        status_code = 503
        
    return {"status_code": status_code}

#################################################Verify User##############################################
def verify_user(username):
    engine = db_conn.db_engine()
    status_code = None
    if engine:
        Session = sessionmaker(bind=db_conn.db_engine())
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        user.verified = True
        session.commit()
        session.close()
        status_code = 204
    else:
        status_code = 503
        
    return {"status_code": status_code}

