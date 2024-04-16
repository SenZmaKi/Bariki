#!/usr/bin/env python3
""" Module with database functions """
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.donor import Donor
from models.recipient import Recipient
from models.cause import Cause
from models.contract import Contract


class DB:
    """ Interacts with the SQLite / MYSQL database """
    __session = None
    __engine = None

    def __init__(self):
        """ Init vars """
        self.__engine = create_engine("sqlite:///bariki.db")
        # add session

    def new(self, obj):
        """ Add new object to database session"""
        self.__session.add(obj)
        self.save()
    
    def save(self):
        """ Commit changes made to db"""
        self.__session.commit()

    def get(self, cls, **kwargs):
        """ Queries database & returns object if found else None"""
        pass

    def delete(self, obj):
        """ Delete an object from db """
        self.__session.remove(obj)
        self.save()

    def 
