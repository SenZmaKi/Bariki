#!/usr/bin/python3
""" Module with model for 'charity cause' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel, db

class Donation(BaseModel, db):
    """ Class with 'cause' entity definition"""
    __tablename__ = 'donations'

    amount = Column(Integer, nullable=False)
    cause_id = Column(Integer, ForeignKey('causes.id'))
    cause = relationship('Cause', back_populates='donations')
    user_id = Column(Integer, ForeignKey('users.id'))
    donor = relationship('User', back_populates='donations')
    # rlships: user, cause (backref used to refer)
