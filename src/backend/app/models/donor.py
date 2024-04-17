""" Model with Donor entity model """
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel, db
from uuid import uuid4 as unique


class Donor(BaseModel, db):
    """ User class Model """
    __tablename__ = 'donors'

    first_name = Column(String(50), nullable=False)
    second_name = Column(string(50), nullable=False)
