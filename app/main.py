from fastapi import FastAPI
from app.core.database import engine
from app.models import ticket
from app.routers.ticket_router import ticket_router

ticket.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ticket Management System",
    description="A comprehensive ticket tracking application",
    version="0.1.0"
)

app.include_router(ticket_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Ticket Management System"}
