from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.utils.auth import get_current_customer, get_current_active_customer
from app.db.database import get_db
from app.db.schemas.booking import BookingCreate, BookingUpdate
from app.api.utils.booking import create_booking, get_bookings, cancel_booking, update_booking


router = APIRouter(tags=["bookings"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/book/")
def book(booking: BookingCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    customer = get_current_customer(db, token)
    active_customer = get_current_active_customer(customer)
    booking_id = create_booking(db, booking, customer_id=active_customer.id)

    if booking_id == -1:
        raise HTTPException(status_code=400, detail="An error occurred while booking")
    return Response(status_code=200, content=f"Success, booking with id={booking_id} is created")


@router.post("/unbook/")
def unbook(booking_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    customer = get_current_customer(db, token)
    active_customer = get_current_active_customer(customer)
    is_canceled = cancel_booking(db, booking_id, customer_id=active_customer.id)

    if not is_canceled:
        raise HTTPException(status_code=403, detail="You are not allowed to cancel booking")
    return Response(status_code=200, content="Success")


@router.put("/update/")
def update(new_booking: BookingUpdate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    customer = get_current_customer(db, token)
    active_customer = get_current_active_customer(customer)
    is_updated = update_booking(db, new_booking, customer_id=active_customer.id)

    if not is_updated:
        raise HTTPException(status_code=404, detail="Booking is not found")
    return Response(status_code=200, content="Success")


@router.get("/list/")
def list_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = get_bookings(db, skip=skip, limit=limit)
    return bookings
