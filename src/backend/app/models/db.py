#!/usr/bin/python3
""" Module with database functions """
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.user import User
from models.cause import Cause
from models.donation import Donation
from models.contract import Contract
from models.base import BaseModel, db


_classes = {"User": User, "Donation": Donation, "Cause": Cause, "Contract": Contract}


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

    def get(self, cls, id):
        """ Returns the object based on the class name and its ID
            or None if not found
        """
        if cls not in _classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value


    def delete(self, obj=None):
        """ Delete an object from db """
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def all(self, cls=None):
        """ Returns all objects of a certain class
            e.g cls=<Donor> returns all donors
        """
        all_objs = {}
        for clss in _classes:
            if cls is None or cls is _classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def reload(self):
        """reloads data from the database"""
        db.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """ close current db session """
        self.__session.remove()

    def count(self, cls=None):
        """ count the number of objects in storage
            cls: count objects in a specific class
        """
        all_class = _classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())
        return count

    def flush_database(self):
        """ Flush database """
        db.metadata.drop_all(self.__engine)
