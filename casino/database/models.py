from sqlalchemy import Column, String
from casino.database.db import Base

class User(Base):
    __tablename__ = 'users'

    username = Column(String(255), primary_key=True)
