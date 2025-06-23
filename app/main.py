# main.py - FastAPI application entrypoint
from fastapi import FastAPI
from app.routers import customers, payments, risk

app = FastAPI(title="Payments API")

# Include modular routes
app.include_router(customers.router)
app.include_router(payments.router)
app.include_router(risk.router)

@app.get("/")
def root():
    return {"message": "Payments API is running"}
