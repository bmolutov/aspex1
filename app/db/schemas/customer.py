from pydantic import BaseModel
from booking import Booking


class CustomerBase(BaseModel):
    email: str


class CustomerCreate(CustomerBase):
    password: str


class Customer(CustomerBase):
    id: int
    name: str
    phone: str
    is_active: bool

    bookings: list[Booking] = []

    class Config:
        orm_mode = True
