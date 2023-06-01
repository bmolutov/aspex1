from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.schemas.customer import CustomerCreate
from app.db.database import get_db
from app.api.utils.customer import get_customer_by_email, create_customer, get_customer_bookings
from app.api.utils.auth import get_current_active_customer, get_current_customer


router = APIRouter(tags=["customers"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register/")
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_customer(db=db, customer=customer)


@router.get("/bookings/")
def list_customer_bookings(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)):
    customer = get_current_customer(db, token)
    active_customer = get_current_active_customer(customer)
    return get_customer_bookings(db, active_customer.id)
