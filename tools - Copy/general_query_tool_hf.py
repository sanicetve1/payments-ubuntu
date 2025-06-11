# tools/general_query_tool.py

import requests
from pydantic import BaseModel
from langchain.tools import StructuredTool

BASE_URL = "http://localhost:8000"

# 🧾 Tool 1: Get all customers
class EmptyInput(BaseModel):
    pass

def get_customers(_: EmptyInput):
    return requests.get(f"{BASE_URL}/customers").json()

get_customers_tool = StructuredTool.from_function(
    name="get_customers",
    description="Get a list of all customers in the system.",
    func=get_customers
)

# 🧾 Tool 2: Get customer by ID
class CustomerByIdInput(BaseModel):
    customer_id: str

def get_customer_by_id(input: CustomerByIdInput):
    return requests.get(f"{BASE_URL}/customers/{input.customer_id}").json()

get_customer_by_id_tool = StructuredTool.from_function(
    name="get_customer_by_id",
    description="Fetch details of a customer using their ID.",
    func=get_customer_by_id
)

# 💳 Tool 3: Get payments by method (e.g., card)
class PaymentMethodInput(BaseModel):
    method: str

def get_payments_by_method(input: PaymentMethodInput):
    return requests.get(f"{BASE_URL}/payments", params={"method": input.method}).json()

get_payments_by_method_tool = StructuredTool.from_function(
    name="get_payments_by_method",
    description="Get all payments filtered by payment method (e.g., card, klarna).",
    func=get_payments_by_method
)

# 💸 Tool 4: Get payments made by a customer
class CustomerPaymentsInput(BaseModel):
    customer_id: str

def get_customer_payments(input: CustomerPaymentsInput):
    return requests.get(f"{BASE_URL}/customers/{input.customer_id}/payments").json()

get_customer_payments_tool = StructuredTool.from_function(
    name="get_customer_payments",
    description="Get all payments made by a specific customer.",
    func=get_customer_payments
)

# ⚠️ Tool 5: Get flagged customers (fraud/disputes)
def get_flagged_customers(_: EmptyInput):
    return requests.get(f"{BASE_URL}/risk/flagged").json()

get_flagged_customers_tool = StructuredTool.from_function(
    name="get_flagged_customers",
    description="Retrieve a list of customers with fraudulent or disputed transactions.",
    func=get_flagged_customers
)

# 🔧 Tool registry for LangGraph or agent execution
all_tools = [
    get_customers_tool,
    get_customer_by_id_tool,
    get_payments_by_method_tool,
    get_customer_payments_tool,
    get_flagged_customers_tool
]
