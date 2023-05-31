from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.customer import Customer
from app.db.schemas.customer import CustomerInDB
from app.db.models.booking import Booking


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerInDB):
    # todo: how to hash password?
    fake_hashed_password = customer.password + "notreallyhashed"
    db_customer = Customer(email=customer.email, hashed_password=fake_hashed_password)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def add_booking_to_customer(db: Session, customer_id: int, booking_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not customer or not booking:
        raise HTTPException(status_code=404, detail='Customer or Booking not found')

    customer.bookings.append(booking)
    db.commit()
    db.refresh(customer)
    return {"message": "Booking added to customer successfully"}


def remove_booking_from_customer(db: Session, customer_id: int, booking_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not customer or not booking:
        raise HTTPException(status_code=404, detail='Customer or Booking not found')

    customer.bookings.remove(booking)
    db.commit()
    db.refresh(customer)
    return {"message": "Booking removed from customer successfully"}
