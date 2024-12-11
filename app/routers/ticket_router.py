from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from crouton import SQLAlchemyCRUDRouter
from app.core.database import get_db
from app.models.ticket import Ticket, TicketStatus, TicketPriority
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from typing import Dict, Any, List, Optional

class CustomTicketRouter(SQLAlchemyCRUDRouter):
    def add_api_route(self, path, endpoint, **kwargs):
        if path == "/stats":
            kwargs['response_model'] = Dict[str, Any]
        return super().add_api_route(path, endpoint, **kwargs)

ticket_router = CustomTicketRouter(
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
        
        priority_counts = (
            db.query(Ticket.priority, func.count(Ticket.id))
            .group_by(Ticket.priority)
            .all()
        )
        
        status_breakdown = {
            str(status): count for status, count in status_counts
        }
        
        priority_breakdown = {
            str(priority): count for priority, count in priority_counts
        }
        
        stats = {
            "total_tickets": db.query(Ticket).count(),
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown,
            "ticket_stats": {
                "open_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.OPEN).count(),
                "in_progress_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.IN_PROGRESS).count(),
                "resolved_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.RESOLVED).count(),
                "closed_tickets": db.query(Ticket).filter(Ticket.status == TicketStatus.CLOSED).count(),
            },
            "priority_stats": {
                "low_priority": db.query(Ticket).filter(Ticket.priority == TicketPriority.LOW).count(),
                "medium_priority": db.query(Ticket).filter(Ticket.priority == TicketPriority.MEDIUM).count(),
                "high_priority": db.query(Ticket).filter(Ticket.priority == TicketPriority.HIGH).count(),
                "critical_priority": db.query(Ticket).filter(Ticket.priority == TicketPriority.CRITICAL).count(),
            }
        }
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ticket_router.get("/{item_id}", response_model=Optional[TicketResponse])
def read_ticket(item_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == item_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
