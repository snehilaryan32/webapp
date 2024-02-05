from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    account_created = Column(DateTime, default=datetime.datetime.now)
    account_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now)