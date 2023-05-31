from pydantic import BaseModel
from booking import BookingSchema


class CustomerBase(BaseModel):
    email: str


class CustomerInDB(CustomerBase):
    hashed_password: str


class CustomerSchema(CustomerBase):
    id: int
    name: str
    phone: str
    is_active: bool

    bookings: list[BookingSchema] = []

    class Config:
        orm_mode = True
