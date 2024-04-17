#!/usr/bin/python3
"""Module with database functions"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models.user import User
from app.models.cause import Cause
from app.models.base import decl_base
from app.models.donation import Donation


_classes = {"Cause": Cause, "User": User, "Donation": Donation}

class DB:
    """Interacts with the SQLite database"""

    def __init__(self):
        """Init vars"""
        self._engine = create_engine("sqlite:///bariki.db")
        self.reload()

    def add(self, obj):
        """Add new object to database session"""
        self.session.add(obj)
        self.save()

    def save(self):
        """Commit changes made to db"""
        self.session.commit()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID
        or None if not found
        """
        obj = self.session.query(cls).filter_by(id=id).first()
        return obj

    def delete(self, obj=None):
        """Delete an object from db"""
        if obj is not None:
            self.session.delete(obj)
            self.save()

    def all(self, cls=None):
        """Returns all objects of a certain class
        e.g cls=<User> returns all users
        """
        new_dict = {}
        for cls in _classes:
            if cls is None or cls is _classes[cls] or cls is cls:
                objs = self.session.query(_classes[cls]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def reload(self):
        """Reloads data from the database"""
        decl_base.metadata.create_all(self._engine)
        sess_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.session = Session

    def close(self):
        """close current db session"""
        self.session.remove()

    def count(self, cls=None):
        """count the number of objects in storage
        cls: count objects in a specific class
        """
        if not cls:
            count = 0
            for clas in _classes.values():
                count += self.count(clas)
        else:
            count = self.session.query(cls).count()
        return count

    def flush_database(self):
        """Flush database"""
        decl_base.metadata.drop_all(self._engine)
