import db_conn
from models.user import User, Base
from sqlalchemy.orm import sessionmaker


def create_user(email, first_name, last_name, password):
    engine = db_conn.db_engine()
    if engine:
        try:
            Session = sessionmaker(bind=db_conn.db_engine())
            session = Session()
            new_user = User(username=email, first_name=first_name, last_name=last_name, password=password)
            session.add(new_user)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False



#test code    
# create_user("jackie@benrandis.com", "jackie", "vernor", "password1234")