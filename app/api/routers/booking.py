from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.schemas.booking import BookingCreate, BookingSchema
from app.api.utils.booking import create_booking, get_bookings


router = APIRouter(prefix='/bookings')


@router.post("/create/")
def book(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking)


@router.get("/list/")
def list_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = get_bookings(db, skip=skip, limit=limit)
    return bookings
