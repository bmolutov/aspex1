from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db.schemas.customer import CustomerSchema, CustomerCreate
from app.db.schemas.booking import TableSchema
# from app.main import get_db
from app.db.database import get_db
from app.api.utils.customer import get_customer_by_email, create_customer, get_customer_bookings
from app.api.utils.auth import get_current_active_user


router = APIRouter(prefix='/customers')


# todo: error
# @router.get("/customers/me/", CustomerSchema)
# async def read_users_me(
#         current_user: Annotated[CustomerSchema, Depends(get_current_active_user)]
# ):
#     return current_user


@router.post("/register/", response_model=CustomerSchema)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_customer(db=db, customer=customer)


@router.get("/bookings/")
def list_customer_bookings(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_bookings(db, customer_id)
