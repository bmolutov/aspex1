from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import text
from fastapi import HTTPException
from datetime import datetime

from app.db.models.booking import Booking, Table
from app.db.schemas.booking import BookingCreate, BookingUpdate


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(Booking.is_active).options(joinedload(Booking.tables)).offset(skip).limit(limit).all()


def get_bookings_of_customer(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(customer_id=customer_id, is_active=True).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate, customer_id: int):
    booking_dict = booking.dict()
    booking_dict['customer_id'] = customer_id
    tables = booking_dict.pop("tables", None)
    db_booking = Booking(**booking_dict)

    query = text(
        """
        SELECT booking_table.table_id
        FROM booking_table
            LEFT OUTER JOIN bookings ON booking_table.booking_id = bookings.id
        WHERE bookings.is_active = true
        GROUP BY booking_table.table_id
        HAVING MAX(bookings.booking_time_end) <= (SELECT NOW())
        UNION
        SELECT id FROM tables
        WHERE id NOT IN (
            SELECT table_id FROM booking_table 
        ) AND is_active = true;
        """
    )
    rows = db.execute(query)
    unbooked_tables = [row[0] for row in rows]
    unbooked_tables = [val for val in unbooked_tables if val in tables]

    # we cannot book when there is no unbooked tables from input
    if not unbooked_tables:
        return -1

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    for table_id in unbooked_tables:
        add_table_to_booking(db, booking_id=db_booking.id, table_id=table_id)

    return db_booking.id


def cancel_booking(db: Session, booking_id: int, customer_id: int):
    booking = db.query(Booking).filter(
        Booking.id == booking_id, Booking.customer_id == customer_id, Booking.is_active
    ).first()
    if not booking:
        return False
    time_diff = datetime.now() - booking.booking_time_start
    minutes_diff = time_diff.total_seconds() // 60

    if minutes_diff > 60:
        return False

    booking.is_active = False
    db.commit()
    db.refresh(booking)
    return True


def update_booking(db: Session, new_booking: BookingUpdate, customer_id: int):
    booking = db.query(Booking).filter(
        Booking.id == new_booking.id, Booking.customer_id == customer_id, Booking.is_active
    ).first()
    if not booking:
        return False
    booking.booking_time_start = new_booking.booking_time_start
    booking.booking_time_end = new_booking.booking_time_end
    db.commit()
    db.refresh(booking)
    return True


def add_table_to_booking(db: Session, booking_id: int, table_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.is_active).first()
    table = db.query(Table).filter(Table.id == table_id, Table.is_active).first()

    if not booking or not table:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    booking.tables.append(table)
    db.commit()
    db.refresh(booking)
    return {"message": "Table added to booking successfully"}


def remove_table_from_booking(db: Session, booking_id: int, table_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.is_active).first()
    table = db.query(Table).filter(Table.id == table_id, Table.is_active).first()

    if not booking or not table:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    booking.tables.remove(table)
    db.commit()
    db.refresh(booking)
    return {"message": "Table removed from booking successfully"}
