from typing import List
from pydantic import BaseModel

from app.db.schemas.booking import BookingSchema


class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    name: str
    phone: str
    is_active: bool
    password: str


class CustomerSchema(CustomerBase):
    id: int
    name: str
    phone: str
    is_active: bool

    bookings: List["BookingSchema"] = []

    class Config:
        orm_mode = True
