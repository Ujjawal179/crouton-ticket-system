from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from crouton import SQLAlchemyCRUDRouter
from app.core.database import get_db
from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from typing import Dict, Any

ticket_router = SQLAlchemyCRUDRouter(
    schema=TicketResponse,
    create_schema=TicketCreate,
    update_schema=TicketUpdate,
    db_model=Ticket,
    db=get_db,
    prefix='tickets'
)

@ticket_router.get("/stats", response_model=Dict[str, Any])
def get_ticket_stats(db: Session = Depends(get_db)):
    try:
        status_counts = (
            db.query(Ticket.status, func.count(Ticket.id))
            .group_by(Ticket.status)
            .all()
        )
        
        status_breakdown = {
            str(status): count for status, count in status_counts
        }
        
        stats = {
            "total_tickets": db.query(Ticket).count(),
            "status_breakdown": status_breakdown,
            "ticket_stats": {
                "open_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.OPEN).count(),
                "in_progress_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.IN_PROGRESS).count(),
                "resolved_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.RESOLVED).count(),
                "closed_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.CLOSED).count(),
            }
        }
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
