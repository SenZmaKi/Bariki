#!/usr/bin/python3
""" Module with model for 'charity cause' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models.base import BaseModel, db

class Cause(BaseModel, db):
    """ Class with 'cause' entity definition"""
    __tablename__ = 'causes'

    name = Column(String(60), nullable=False)
    description = Column(Text)
    recipient_id = Column(Integer, ForeignKey('recipients.id'), nullable=False)
    # contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
