""" Model with recipient entity model """
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel, db

class Recipient(BaseModel, db):
    """ recipient entity Model class"""
    __tablename__ = 'recipients'

    first_name = Column(String(50), nullable=False)
    second_name = Column(string(50), nullable=False)
