from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import time

from app.db.database import Base

booking_table = Table('booking_table', Base.metadata,
                      Column('booking_id', ForeignKey('bookings.id'), primary_key=True),
                      Column('table_id', ForeignKey('tables.id'), primary_key=True)
                      )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_time_start = Column(DateTime, default=time(14, 0))
    booking_time_end = Column(DateTime, default=time(17, 0))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="bookings")
    tables = relationship("Table", secondary="booking_table", back_populates="bookings")


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, default=2)
    available_time_start = Column(DateTime, default=time(12, 0))
    available_time_end = Column(DateTime, default=time(22, 0))

    bookings = relationship("Booking", secondary="booking_table", back_populates="tables")
