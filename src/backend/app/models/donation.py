#!/usr/bin/python3
""" Module with model for 'charity cause' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models.base import BaseModel, db

class Donation(BaseModel, db):
    """ Class with 'cause' entity definition"""
    __tablename__ = 'donations'

    amount = Column(Integer, nullable=False)
    # rlships: user, cause (backref used to refer)
