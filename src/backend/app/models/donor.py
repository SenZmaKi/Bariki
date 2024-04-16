""" Model with Donor entity model """
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import db
from datetime import datetime
from uuid import uuid4 as unique

class User(db.Model):
    """ User class Model """
    __tablename__ = 'donors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    second_name = Column(string(50), nullable=False)
    public_address = Column(String(100), default=self.new_address())

    def _new_address(self) -> str:
        """ Returns a random public address for a new user """
        return unique()
