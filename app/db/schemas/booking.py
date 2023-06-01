from typing import List
from pydantic import BaseModel
from datetime import datetime


class TableBase(BaseModel):
    capacity: int
    available_time_start: datetime
    available_time_end: datetime


class TableCreate(TableBase):
    pass


class BookingBase(BaseModel):
    customer_id: int
    booking_time_start: datetime
    booking_time_end: datetime


class BookingCreate(BookingBase):
    tables: List[int] = []


class Table(TableBase):
    id: int


class Booking(BookingBase):
    id: int


# final schemas
class TableSchema(Table):
    bookings: List[BookingBase] = []

    class Config:
        orm_mode = True


class BookingSchema(Booking):
    tables: List[TableBase] = []

    class Config:
        orm_mode = True
