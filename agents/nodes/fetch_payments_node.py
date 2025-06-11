# agents/nodes/fetch_payments_node.py
from typing import Dict
from langchain_core.runnables import RunnableConfig
from tools.api_tools import fetch_payments_by_method

def payment_node(state: Dict, config: RunnableConfig) -> Dict:
    query_type = state.get("query_type")
    entity = state.get("entity")

    if query_type == "payments_by_method" and entity:
        return {"result": fetch_payments_by_method(entity)}

    return {"error": f"Unsupported payment query_type: {query_type}"}
