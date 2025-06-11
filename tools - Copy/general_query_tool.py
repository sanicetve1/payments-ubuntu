# tools/general_query_tool.py

import requests
from langchain.tools import Tool

BASE_URL = "http://localhost:8000"

def generalized_query(query_type: str, entity: str = None):
    print(f"🔍 [INFO] Query Type Received: '{query_type}' | Entity: '{entity}'")

    try:
        if query_type == "customers":
            response = requests.get(f"{BASE_URL}/customers")

        elif query_type == "payments_by_method" and entity:
            response = requests.get(f"{BASE_URL}/payments", params={"method": entity})

        elif query_type == "customer_payments" and entity:
            response = requests.get(f"{BASE_URL}/customers/{entity}/payments")

        elif query_type == "flagged_customers":
            response = requests.get(f"{BASE_URL}/risk/flagged")

        elif query_type == "customer_by_id" and entity:
            response = requests.get(f"{BASE_URL}/customers/{entity}")

        else:
            return {"error": "Unsupported query_type or missing entity"}

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except Exception as ex:
        return {"error": "Unexpected error occurred"}


general_tool = Tool.from_function(
    name="general_query_tool",
    description=(
        "A generalized tool to query payments and customers. "
        "query_type can be: 'customers', 'payments_by_method', 'customer_payments', "
        "'flagged_customers', or 'customer_by_id'. "
        "Use 'entity' for methods like 'card' or customer ID."
    ),
    func=generalized_query
)
