#!/usr/bin/python3
"""Model with Donor entity model"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import decl_base
from app.models.donation import WithDonationsFields
from flask_login import UserMixin


class User(UserMixin, WithDonationsFields, decl_base):
    """User class Model"""

    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile_pic_url = Column(String, nullable=True)
    algo_account_address = Column(String, nullable=True) # TODO change nullable to false
    bank_creds = Column(String, nullable=True)  # encrypt?
   # is_active = Column(Boolean, default=False)
    # is_authenticated = Column(Boolean, default=False)
    causes = relationship("Cause", back_populates="initiator")
    donations = relationship("Donation", back_populates="donor")  # pyright: ignore
