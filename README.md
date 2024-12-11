# Ticket Management System

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Features
- Create, Read, Update, Delete tickets
- Ticket status and priority management
- Basic ticket statistics

## API Documentation
Access Swagger UI at: `http://localhost:8000/docs`