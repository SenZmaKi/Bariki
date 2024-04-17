from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import AddressModel, decl_base


class Cause(AddressModel, decl_base):
    """Class with 'cause' model definition"""

    def __init__(self, **kwargs):
        if isinstance(kwargs["deadline"], str):
            kwargs["deadline"] = datetime.fromisoformat(kwargs["deadline"])
        super().__init__(**kwargs)

    __tablename__ = "causes"

    name = Column(String(60), nullable=False)
    description = Column(Text)
    image_url = Column(String)
    current_amount = Column(Integer, default=0)
    goal_amount = Column(Integer)
    deadline = Column(Date)
    algo_account_address = Column(String)
    donations = relationship("Donation", back_populates="cause")
    is_ongoing = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    initiator = relationship("User", back_populates="causes")

    def __repr__(self):
        return f"Cause(id={self.id}, name={self.name}"
