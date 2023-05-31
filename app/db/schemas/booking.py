from pydantic import BaseModel
from datetime import datetime


class TableBase(BaseModel):
    id: int
    capacity: int
    available_time_start: datetime
    available_time_end: datetime
    is_booked: bool

    class Config:
        orm_mode = True


class TableCreate(BaseModel):
    pass


class BookingBase(BaseModel):
    id: int
    customer_id: int
    booking_time_start: datetime
    booking_time_end: datetime

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


# final schemas
class Table(TableBase):
    bookings: list[BookingBase] = []


class Booking(BookingBase):
    tables: list[TableBase] = []
