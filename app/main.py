from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.db.database import engine, Base
from app.api.routers import auth, customer, table, booking

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customer.router)
app.include_router(auth.router)
app.include_router(table.router)
app.include_router(booking.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="aspex1",
        version="1.0",
        description="aspex pet project",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
