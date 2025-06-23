# tools/api_tools.py
from langchain.tools import Tool
import requests
import logging
import ast
from tools.time_tools import time_tools
from tools.rag_tool import rag_tool

print("enter api_tools.py")

BASE_URL = "http://localhost:8000"

def fetch_customers(_=None):
    return requests.get(f"{BASE_URL}/customers").json()

def fetch_customers_by_ids(customer_ids):
    if isinstance(customer_ids, str):
        try:
            customer_ids = ast.literal_eval(customer_ids)
        except Exception as e:
            print("❌ Failed to parse string to list:", e)
            return []

    customers = []
    for cid in customer_ids:
        try:
            res = requests.get(f"{BASE_URL}/customers/{cid}")
            if res.status_code == 200:
                customers.append(res.json())
            else:
                print(f"⚠️ Customer {cid} not found")
        except Exception as e:
            print(f"❌ Error fetching {cid}: {e}")
    return customers


def fetch_payments_by_method(method: str):
    print("fetch payments by method is called ")
    method = method.strip().lower().replace("'", "")
    print("🔍 Payment method filter triggered with:", method)
    try:
        response = requests.get(f"{BASE_URL}/payments", params={"method": method})
        response.raise_for_status()
        data = response.json()
        print(f"📦 API responded with {len(data)} items. Raw: {data}")
        return data
    except Exception as e:
        print("❌ Failed to fetch payments:", e)
        return []

def fetch_customer_payments(customer_id: str):
    return requests.get(f"{BASE_URL}/customers/{customer_id}/payments").json()

def fetch_flagged_customers(_=None):
    return requests.get(f"{BASE_URL}/risk/flagged").json()

print("🛠 calling get_payments_by_method tool")
tools = time_tools + [
    Tool.from_function(
        name="get_customers",
        description="Fetch all customer profiles",
        func=fetch_customers
    ),
    Tool.from_function(
        name="get_payments_by_method",
        description="Fetch all payments for a given method like 'card', 'cash', 'alipay' or 'klarna'. "
        "Returns payment records that include 'customer_id', which can be used "
        "with 'fetch_customers_by_ids' to get the full customer details.",
        func=fetch_payments_by_method,
    ),
    Tool.from_function(
        name="get_customer_payments",
        description="Fetch payments made by a customer using their ID",
        func=fetch_customer_payments
    ),
    Tool.from_function(
        name="get_flagged_customers",
        description="Fetch customers with fraudulent or disputed payments",
        func=fetch_flagged_customers
    ),
    Tool.from_function(
        name="fetch_customers_by_ids",
        description= "Fetch full customer details given a list of customer_ids. "
        "Use this after calling 'get_payments_by_method' or other functions that return customer_ids.",
        func=fetch_customers_by_ids
    ),
    rag_tool
]
