from sqlalchemy import ForeignKey, String, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base = declarative_base()

class EmailTracker(Base):
    __tablename__ = 'email_tracker'
    email_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verification_token = Column(String)
    email = Column(String)
    sent_time = Column(DateTime, default=datetime.datetime.now)