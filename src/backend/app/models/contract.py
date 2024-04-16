""" Module with model for 'contract' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models.base import db
from datetime import datetime
from uuid import uuid4 as unique

class Contract(db.Model):
    """ Class with 'contract' entity definition"""
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    recipient_id = Column(Integer, ForeignKey('recipients.id'), nullable=False)
