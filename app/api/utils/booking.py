from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.booking import Booking, Table
from app.db.schemas.booking import BookingCreate


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()


def get_bookings_of_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(customer_id=customer_id).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate, customer_id: int):
    db_booking = Booking(**booking.dict(), customer_id=customer_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def add_table_to_booking(db: Session, booking_id: int, table_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    table = db.query(Table).filter(Table.id == table_id).first()

    if not booking or not table:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    booking.tables.append(table)
    db.commit()
    db.refresh(booking)
    return {"message": "Table added to booking successfully"}


def remove_table_from_booking(db: Session, booking_id: int, table_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    table = db.query(Table).filter(Table.id == table_id).first()

    if not booking or not table:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    booking.tables.remove(table)
    db.commit()
    db.refresh(booking)
    return {"message": "Table removed from booking successfully"}
