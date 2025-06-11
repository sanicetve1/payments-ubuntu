# agents/nodes/route_node.py
import re
from langchain_core.runnables import RunnableConfig
from typing import Dict

def route_node(inputs: Dict, config: RunnableConfig) -> Dict:
    """
    LangGraph routing node that parses user input and returns query_type + entity
    in the graph state. Uses keyword + regex extraction.
    """
    user_input = inputs.get("input", "").lower()
    print("📥 Full Inputs Received:", inputs)
    print("🌝 Routing input:", user_input)

    # Extract customer ID if present
    customer_id_match = re.search(r"cus_[a-zA-Z0-9]+", user_input)
    customer_id = customer_id_match.group() if customer_id_match else None

    if "card" in user_input:
        return {
            "query_type": "payments_by_method",
            "entity": "card"
        }
    elif "flagged" in user_input or "fraud" in user_input:
        return {
            "query_type": "flagged_customers"
        }
    elif "customer id" in user_input and customer_id:
        return {
            "query_type": "customer_by_id",
            "entity": customer_id
        }
    elif "all customers" in user_input or "list customers" in user_input:
        return {
            "query_type": "customers"
        }
    elif "payments made by" in user_input and customer_id:
        return {
            "query_type": "customer_payments",
            "entity": customer_id
        }
    else:
        print("⚠️ Unrecognized input, falling back.")
        return {
            "query_type": "fallback",
            "entity": None
        }
