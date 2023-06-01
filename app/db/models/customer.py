from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="customer")
