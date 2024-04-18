#!/usr/bin/python3
"""Base models"""

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base
import uuid
from app import algo
from datetime import UTC, datetime
from app import models


decl_base = declarative_base()
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def get_current_utc_time():
    return datetime.now(UTC)


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=get_current_utc_time)
    updated_at = Column(DateTime, default=get_current_utc_time)

    def __init__(self, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def update(self):
        """Updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = get_current_utc_time()
        models.database.add(self)
        models.database.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        _dict = self.__dict__.copy()
        _dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        if "hashed_password" in _dict:
            del _dict["hashed_password"]
        for k, v in _dict.items():
            if isinstance(v, datetime):
                _dict[k] = v.isoformat()
        return _dict

    def delete(self):
        """delete the current instance from the storage"""
        models.database.delete(self)


class AddressModel(BaseModel):
    """
    Parent class for models that have algorant accounts i.e., user, cause
    """

    def __init__(self, **kwargs):
        self.algo_account_address = algo.create_account()
        super().__init__(**kwargs)
