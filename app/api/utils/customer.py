from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException, Response

from app.db.models.customer import Customer
from app.db.schemas.customer import CustomerCreate
from app.db.models.booking import Booking, Table


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerCreate):
    from app.api.utils.auth import get_password_hash
    # todo: check hashing in future
    hashed_password = get_password_hash(customer.password)
    try:
        db_customer = Customer(email=customer.email, hashed_password=hashed_password)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return Response(status_code=201, content="Customer created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")


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


def get_customer_bookings(db: Session, customer_id: int):
    query = text(
        """
        SELECT id, capacity, available_time_start, available_time_end
        FROM tables
        WHERE id IN (
            SELECT booking_table.table_id
            FROM booking_table
                INNER JOIN bookings ON booking_table.booking_id = bookings.id
            WHERE bookings.customer_id = :customer_id
            GROUP BY booking_table.table_id
            HAVING MAX(bookings.booking_time_end) > (SELECT NOW())
        );
        """
    )
    rows = db.execute(query, {"customer_id": customer_id})
    tables = [Table(id=row[0], capacity=row[1], available_time_start=row[2], available_time_end=row[3]) for row in rows]
    return tables
