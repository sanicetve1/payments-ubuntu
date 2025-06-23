# routers/payments.py
from fastapi import APIRouter, Query
from typing import List
from app.db import query_db
from app.models import Payment

router = APIRouter()
print("📥 /payments endpoint hit")

@router.get("/payments")
def get_payments_by_method(method: str = Query(None)):
    print(f"🔍 Received method param: {method}")
    if method:
        cleaned = method.strip().lower().replace("'", "")
        results = query_db(
            "SELECT * FROM payments WHERE LOWER(payment_method) LIKE ?", (f"%{cleaned}%",)
        )
        print(f"✅ DB returned {len(results)} rows for '{cleaned}'")
        return results
    return query_db("SELECT * FROM payments")


@router.get("/customers/{customer_id}/payments", response_model=List[Payment])
def get_payments_for_customer(customer_id: str):
    return query_db("SELECT * FROM payments WHERE customer_id = ?", (customer_id,))


@router.get("/payments/recent")
def get_recent_payments(after: int = Query(..., description="Timestamp after which payments were made")):
    return query_db("SELECT * FROM payments WHERE created >= ?", (after,))
