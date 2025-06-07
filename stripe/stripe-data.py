# file: main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Load Stripe test secret key
stripe.api_key = os.getenv("STRIPE_API_KEY")

app = FastAPI()

print("the loaded ap key", os.getenv("STRIPE_API_KEY"))

@app.get("/stripe/test-payments")
async def get_test_payments(limit: int = 10):
    try:
        # Fetch recent PaymentIntent objects from Stripe sandbox
        payments = stripe.PaymentIntent.list(limit=limit)

        # Format response
        response = [
            {
                "id": p.id,
                "amount": p.amount / 100,  # Convert from cents
                "currency": p.currency,
                "status": p.status,
                "created": p.created,
                "description": p.get("description", ""),
            }
            for p in payments.data
        ]

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
