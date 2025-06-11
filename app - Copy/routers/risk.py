# routers/risk.py
from fastapi import APIRouter
from typing import List
from app.db import query_db
from app.models import Customer

router = APIRouter()

@router.get("/risk/flagged", response_model=List[Customer])
def get_flagged_customers():
    return query_db("""
        SELECT DISTINCT c.*
        FROM customers c
        JOIN payments p ON c.id = p.customer_id
        WHERE p.is_fraudulent = 1 OR p.disputed = 1
    """)
