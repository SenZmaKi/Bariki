""" Module with model for 'charity cause' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models.base import db
from datetime import datetime
from uuid import uuid4 as unique

class Cause(db.Model):
    """ Class with 'cause' entity definition"""
    __tablename__ = 'causes'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text)
    recipient_id = Column(Integer, ForeignKey('recipients.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
