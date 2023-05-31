from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.schemas.customer import CustomerSchema, CustomerInDB
from app.main import get_db, app
from app.api.utils.customer import get_customer_by_email, create_customer
from app.api.utils.auth import get_current_active_user


@app.get("/customers/me/", response_model=CustomerSchema)
async def read_users_me(
        current_user: Annotated[CustomerSchema, Depends(get_current_active_user)]
):
    return current_user


@app.post("/customers/", response_model=CustomerSchema)
def create_customer(customer: CustomerInDB, db: Session = Depends(get_db)):
    db_customer = get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_customer(db=db, customer=customer)
