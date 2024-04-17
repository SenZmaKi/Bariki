#!/usr/bin/python3
"""Base model"""

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
import uuid
from app import models
from datetime import datetime


decl_base = declarative_base()
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs["created_at"], TIME_FORMAT)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], TIME_FORMAT)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.database.add(self)
        # models.storage.save() -- add save after new in method

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        # if "created_at" in new_dict:
        #     new_dict["created_at"] = new_dict["created_at"].strftime(time)
        # if "updated_at" in new_dict:
        #     new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]  # sqlalchemy added
        if "password" in new_dict:
            del new_dict["password"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.database.delete(self)
