#!/usr/bin/python3
""" Model with Donor entity model """
<<<<<<< HEAD
from sqlalchemy import Column, String
=======
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel, db
from .cause import Cause
from .donation import Donation
>>>>>>> c688047d6f60761ebf74424bbd387cd5af3564fe
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, decl_base


class User(BaseModel, decl_base):
    """ User class Model """
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False)
    profile_pic_url = Column(String, nullable=True)
    algo_account_address = Column(String, nullable=False)
    bank_creds = Column(String, nullable=True)  # encrypt?
    causes = relationship('Cause', back_populates='initiator')
    donations = relationship('Donation', back_populates='donor')
