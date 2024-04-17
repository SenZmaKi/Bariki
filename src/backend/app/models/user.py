#!/usr/bin/python3
""" Model with Donor entity model """
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel, db
from models.cause import Cause
from models.donation import Donation
from sqlalchemy.orm import relationship


class User(BaseModel, db):
    """ User class Model """
    __tablename__ = 'donors'

    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False)
    profile_pic_url = Column(String, nullable=True)
    algo_account_address = Column(String, nullable=False)
    bank_creds = Column(String, nullable=True)  # encrypt?
    causes = relationship('Cause', back_populates='initiator')
    donations = relationship('Donation', back_populates='donor')
