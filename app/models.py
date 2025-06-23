# models.py
from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    id: str
    name: str
    email: str
    segment: str
    country: str
    created_at: int

class Payment(BaseModel):
    id: str
    customer_id: str
    amount: int
    currency: str
    payment_method: str
    status: str
    description: str
    metadata_note: Optional[str]
    is_fraudulent: bool
    disputed: bool
    created: int
