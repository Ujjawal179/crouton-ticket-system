from app.core.database import SessionLocal, engine
from app.models.ticket import Ticket, TicketStatus, TicketPriority
import random

def seed_tickets():
    db = SessionLocal()

    try:
        db.query(Ticket).delete()

        sample_tickets = [
            Ticket(
                title=f"Ticket {i}",
                description=f"Description for ticket {i}",
                status=random.choice(list(TicketStatus)),
                priority=random.choice(list(TicketPriority)),
                assignee_id=random.randint(1, 5) if random.random() > 0.5 else None,
                estimated_resolution_time=random.uniform(1, 24)
            ) for i in range(1, 21)
        ]

        db.add_all(sample_tickets)
        db.commit()
        
        print(f"Seeded {len(sample_tickets)} tickets successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    from app.models import ticket
    ticket.Base.metadata.create_all(bind=engine)
    seed_tickets()
