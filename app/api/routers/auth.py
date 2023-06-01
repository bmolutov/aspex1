from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt # noqa
from sqlalchemy.orm import Session

from app.api.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user
from app.db.schemas.token import Token
# from app.main import get_db
from app.db.database import get_db


router = APIRouter(prefix='/token')


@router.post("/get/", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    customer = authenticate_user(db, form_data.username, form_data.password)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": customer.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
