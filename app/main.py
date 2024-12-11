from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.core.database import engine
from app.models import ticket
from app.routers.ticket_router import ticket_router

ticket.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ticket Management System",
    description="A comprehensive ticket tracking application",
    version="0.1.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors()
        }
    )

app.include_router(ticket_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Ticket Management System"}
