from sqlalchemy import Column, Integer, String, Text, Boolean, Date
from sqlalchemy.orm import relationship
from models.base import BaseModel, db


class Cause(BaseModel, db):
    """Class with 'cause' model definition"""

    __tablename__ = "cause"

    name = Column(String(60), nullable=False)
    description = Column(Text)
    image_url = Column(String)
    current_amount = Column(Integer)
    goal_amount = Column(Integer)
    deadline = Column(Date)
    algo_account_address = Column(String)
    donations = relationship("Donation", back_populates="cause")
    is_ongoing = Column(Boolean)

    def __repr__(self):
        return f"Cause(id={self.id}, name={self.name}"
