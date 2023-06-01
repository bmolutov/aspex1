from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.schemas.booking import BookingCreate, BookingSchema, BookingUpdate
from app.api.utils.booking import create_booking, get_bookings, cancel_booking, update_booking


router = APIRouter(prefix='/bookings')


@router.post("/book/")
def book(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking)


@router.post("/unbook/")
def unbook(booking_id: int, db: Session = Depends(get_db)):
    is_canceled = cancel_booking(db, booking_id)
    if not is_canceled:
        raise HTTPException(status_code=403, detail="You are not allowed to cancel booking")
    return Response(status_code=200, content="Success")


@router.put("/update/")
def update(new_booking: BookingUpdate, db: Session = Depends(get_db)):
    is_updated = update_booking(db, new_booking)
    if not is_updated:
        raise HTTPException(status_code=404, detail="Booking is not found")
    return Response(status_code=200, content="Success")


@router.get("/list/")
def list_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = get_bookings(db, skip=skip, limit=limit)
    return bookings
