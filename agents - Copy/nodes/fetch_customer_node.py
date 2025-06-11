# agents/nodes/fetch_customers_node.py
from typing import Dict
from langchain_core.runnables import RunnableConfig
from tools.api_tools import fetch_customers, fetch_customers_by_ids, fetch_customer_payments, fetch_payments_by_method, fetch_flagged_customers


def customer_node(state: Dict, config: RunnableConfig) -> Dict:
    query_type = state.get("query_type")
    entity = state.get("entity")

    if query_type == "customers":
        return {"result": fetch_customers()}

    elif query_type == "customer_by_id" and entity:
        return {"result": fetch_customers_by_ids([entity])}

    elif query_type == "customer_payments" and entity:
        return {"result": fetch_customer_payments(entity)}

    return {"error": f"Unsupported customer query_type: {query_type}"}
