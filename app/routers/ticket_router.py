from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crouton import SQLAlchemyCRUDRouter
from app.core.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate

ticket_router = SQLAlchemyCRUDRouter(
    schema=TicketResponse,
    create_schema=TicketCreate,
    update_schema=TicketUpdate,
    db_model=Ticket,
    db=get_db,
    prefix='tickets'
)

# Additional custom route
@ticket_router.get("/stats")
def get_ticket_stats(db: Session = Depends(get_db)):
    """
    Get ticket statistics
    """
    total_tickets = db.query(Ticket).count()
    open_tickets = db.query(Ticket).filter(Ticket.status == 'open').count()
    
    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
    }