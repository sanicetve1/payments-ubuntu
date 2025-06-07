# routers/customers.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.db import query_db
from app.models import Customer

router = APIRouter()

@router.get("/customers", response_model=List[Customer])
def get_customers():
    return query_db("SELECT * FROM customers")

@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    result = query_db("SELECT * FROM customers WHERE id = ?", (customer_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result[0]
