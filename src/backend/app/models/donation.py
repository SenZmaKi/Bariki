#!/usr/bin/python3
""" Module with model for 'charity cause' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from app.models.base import BaseModel, decl_base
=======
from .base import BaseModel, db
>>>>>>> c688047d6f60761ebf74424bbd387cd5af3564fe

class Donation(BaseModel, decl_base):
    """ Class with 'cause' entity definition"""
    __tablename__ = 'donations'

    amount = Column(Integer, nullable=False)
    cause_id = Column(Integer, ForeignKey('causes.id'))
    cause = relationship('Cause', back_populates='donations')
    user_id = Column(Integer, ForeignKey('users.id'))
    donor = relationship('User', back_populates='donations')
    # rlships: user, cause (backref used to refer)
