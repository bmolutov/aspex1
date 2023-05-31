from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.booking import Booking, Table
from app.db.schemas.booking import TableCreate


def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Table).offset(skip).limit(limit).all()


def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def add_booking_to_table(db: Session, table_id: int, booking_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not table or not booking:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    table.bookings.append(booking)
    db.commit()
    db.refresh(table)
    return {"message": "Booking added to table successfully"}


def remove_booking_from_table(db: Session, table_id: int, booking_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not table or not booking:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    table.bookings.remove(booking)
    db.commit()
    db.refresh(table)
    return {"message": "Booking removed from table successfully"}
