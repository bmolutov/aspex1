from fastapi import FastAPI

from app.db.database import engine, Base
from app.api.routers import auth, customer, table, booking

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customer.router)
app.include_router(auth.router)
app.include_router(table.router)
app.include_router(booking.router)
