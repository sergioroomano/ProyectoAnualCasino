from sqlalchemy import Column, Integer, String, ForeignKey, Bolean
from db import base

class User(base):
    __tablename__ = 'users'

    username = Column(String)
