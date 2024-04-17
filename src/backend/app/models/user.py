#!/usr/bin/python3
""" Model with Donor entity model """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel, db


class User(BaseModel, db):
    """ User class Model """
    __tablename__ = 'donors'

    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    profile_pic_url = Column(String)
    bank_creds = Column(String)  # encrypt?
    # Define relationship with Cause
    cause_id = Column(Integer, ForeignKey('causes.id'))
    cause = relationship('Cause', back_populates='donors')

    # Define relationship with Donation (assuming a donor can make multiple donations)
    donations = relationship('Donation', back_populates='donor')

