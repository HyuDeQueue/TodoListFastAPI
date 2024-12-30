import uuid

from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
class Payment(Base):
    __tablename__ = 'payment'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    orderCode = Column(String(36), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    paymentDate = Column(DateTime(timezone=True), nullable=False, default=func.now())
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="payments")
