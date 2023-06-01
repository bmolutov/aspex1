from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt # noqa
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.schemas.customer import CustomerSchema
from app.api.utils.customer import get_customer_by_email
from app.db.schemas.token import TokenData

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_customer(db: Session, email: str):
    customer = get_customer_by_email(db, email)
    if customer:
        # todo: check
        return customer


def authenticate_user(db: Session, email: str, password: str):
    customer = get_customer_by_email(db, email)
    if not customer:
        return False
    if not verify_password(password, customer.hashed_password):
        return False
    return customer


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # todo: why 15 minutes?
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_customer(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    customer = get_customer(db, email=token_data.email)
    if customer is None:
        raise credentials_exception
    return customer


def get_current_active_customer(
    current_user: Annotated[CustomerSchema, Depends(get_current_customer)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive customer")
    return current_user
