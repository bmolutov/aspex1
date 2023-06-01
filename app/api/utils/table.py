from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy import text
from fastapi import HTTPException

from app.db.models.booking import Booking, Table
from app.db.schemas.booking import TableCreate


def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Table).offset(skip).limit(limit).all()


# verbose - with info of all bookings related to the tables
def get_tables_verbose(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Table).options(joinedload(Table.bookings)).offset(skip).limit(limit).all()


def get_unbooked_tables(db: Session):
    query = text(
        """
        SELECT id, capacity, available_time_start, available_time_end
        FROM tables
        WHERE id IN (
            SELECT booking_table.table_id
            FROM booking_table
                INNER JOIN bookings ON booking_table.booking_id = bookings.id
            GROUP BY booking_table.table_id
            HAVING MAX(bookings.booking_time_end) <= (SELECT NOW())
        )
        UNION
        SELECT id, capacity, available_time_start, available_time_end 
        FROM tables
        WHERE id NOT IN (
            SELECT table_id FROM booking_table 
        );
        """
    )
    rows = db.execute(query)
    tables = [Table(id=row[0], capacity=row[1], available_time_start=row[2], available_time_end=row[3]) for row in rows]
    return tables


def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


# todo: unnecessary function, it is mirror of add_table_to_booking
def add_booking_to_table(db: Session, table_id: int, booking_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not table or not booking:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    table.bookings.append(booking)
    db.commit()
    db.refresh(table)
    return {"message": "Booking added to table successfully"}


# todo: unnecessary function, it is mirror of remove table from booking
def remove_booking_from_table(db: Session, table_id: int, booking_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not table or not booking:
        raise HTTPException(status_code=404, detail='Booking or Table not found')

    table.bookings.remove(booking)
    db.commit()
    db.refresh(table)
    return {"message": "Booking removed from table successfully"}
