from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    account_created = Column(DateTime)
    account_updated = Column(DateTime)