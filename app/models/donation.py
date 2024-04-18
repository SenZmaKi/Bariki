#!/usr/bin/python3
"""Module with model for 'charity cause' entity"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, decl_base, AddressModel


class Donation(BaseModel, decl_base):
    """Class with 'cause' entity definition"""

    __tablename__ = "donations"

    amount = Column(Integer, nullable=False)
    cause_id = Column(Integer, ForeignKey("causes.id"))
    cause = relationship("Cause", back_populates="donations")
    user_id = Column(Integer, ForeignKey("users.id"))
    donor = relationship("User", back_populates="donations")


class WithDonationsFields(AddressModel):
    donations: list[Donation]

    def to_dict(self):
        _dict = super().to_dict()
        donations_dict = [d.to_dict() for d in self.donations]
        _dict["donations"] = donations_dict
        return _dict
