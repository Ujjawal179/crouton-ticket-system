from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.ticket import TicketStatus, TicketPriority

class TicketCreate(BaseModel):
    """Schema for creating a new ticket"""
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIUM
    assignee_id: Optional[int] = None
    estimated_resolution_time: Optional[float] = None

class TicketUpdate(BaseModel):
    """Schema for updating an existing ticket"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assignee_id: Optional[int] = None
    estimated_resolution_time: Optional[float] = None

class TicketResponse(BaseModel):
    """Schema for returning ticket information"""
    id: int
    title: str
    description: Optional[str]
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: Optional[datetime]
    assignee_id: Optional[int]
    
    class Config:
        from_attributes = True