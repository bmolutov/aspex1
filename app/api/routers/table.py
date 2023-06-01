from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas.booking import TableCreate, TableSchema
from app.api.utils.table import get_unbooked_tables, create_table, get_tables, get_tables_verbose


router = APIRouter(tags=["tables"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/create/", response_model=TableSchema)
def create_table_for_customers(table: TableCreate, token: Annotated[str, Depends(oauth2_scheme)],
                               db: Session = Depends(get_db)):
    return create_table(db=db, table=table)


@router.get("/list/unbooked/")
def list_tables_unbooked(db: Session = Depends(get_db)):
    tables = get_unbooked_tables(db)
    return tables


@router.get("/list/")
def list_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = get_tables(db, skip=skip, limit=limit)
    return tables


@router.get("/list/verbose/")
def list_tables_verbose(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = get_tables_verbose(db, skip=skip, limit=limit)
    return tables
