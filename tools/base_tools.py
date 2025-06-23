from typing import List
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
import requests

BASE_URL = "http://localhost:8000"

# --- Input Schemas ---
class PaymentMethodInput(BaseModel):
    method: str = Field(..., description="Payment method such as 'card', 'cash', 'alipay'")

class CustomerByIDInput(BaseModel):
    customer_id: str = Field(..., description="Customer ID to look up")

class CustomerIDsInput(BaseModel):
    customer_ids: List[str] = Field(..., description="List of customer IDs")

# --- Tool Functions ---
def get_payments_by_method(method: str):
    try:
        response = requests.get(f"{BASE_URL}/payments", params={"method": method.strip().lower()})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_customer_by_id(customer_id: str):
    try:
        response = requests.get(f"{BASE_URL}/customers/{customer_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_customer_payments(customer_id: str):
    try:
        response = requests.get(f"{BASE_URL}/customers/{customer_id}/payments")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_flagged_customers(_: None = None):
    try:
        response = requests.get(f"{BASE_URL}/risk/flagged")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_customers(_: None = None):
    try:
        response = requests.get(f"{BASE_URL}/customers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_customers_by_ids(customer_ids: List[str]):
    customers = []
    for cid in customer_ids:
        try:
            res = requests.get(f"{BASE_URL}/customers/{cid}")
            if res.status_code == 200:
                customers.append(res.json())
            else:
                customers.append({"error": f"Customer {cid} not found"})
        except Exception as e:
            customers.append({"error": str(e)})
    return customers

# --- Structured Tools ---
custom_tools = [
    StructuredTool.from_function(
        name="get_payments_by_method",
        description="Use this to retrieve all payment records made using a specific method such as 'card', 'cash', 'alipay'. Returns a list of payments.",
        func=get_payments_by_method,
        args_schema=PaymentMethodInput,
    ),
    StructuredTool.from_function(
        name="get_customer_by_id",
        description="Use this tool to retrieve full profile details of a specific customer by ID. Helpful for follow-up on a payment or risk check.",
        func=get_customer_by_id,
        args_schema=CustomerByIDInput,
    ),
    StructuredTool.from_function(
        name="get_customer_payments",
        description="Use this to get all payment records made by a single customer. Input is customer ID.",
        func=get_customer_payments,
        args_schema=CustomerByIDInput,
    ),
    StructuredTool.from_function(
        name="get_flagged_customers",
        description="Use this tool to find customers flagged for fraud, disputes, or compliance concerns.",
        func=get_flagged_customers,
        args_schema=None,
    ),
    StructuredTool.from_function(
        name="get_customers",
        description="Use this tool when you need a list of all customers with their basic profile details.",
        func=get_customers,
        args_schema=None,
    ),
    StructuredTool.from_function(
        name="get_customers_by_ids",
        description="Use this to fetch profile details for a list of customer IDs. Typically used after a query that returns multiple customer IDs.",
        func=get_customers_by_ids,
        args_schema=CustomerIDsInput,
    ),
]
