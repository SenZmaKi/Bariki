#!/usr/bin/python3
""" Module with model for 'contract' entity """
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from models.base import BaseModel, db

class Contract(BaseModel, db):
    """ Class with 'contract' entity definition"""
    __tablename__ = 'contracts'

    recipient_id = Column(Integer, ForeignKey('recipients.id'), nullable=False)
