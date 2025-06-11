# agents/nodes/fetch_risk_node.py
from typing import Dict
from langchain_core.runnables import RunnableConfig
from tools.api_tools import fetch_flagged_customers

def risk_node(state: Dict, config: RunnableConfig) -> Dict:
    query_type = state.get("query_type")

    if query_type == "flagged_customers":
        return {"result": fetch_flagged_customers()}

    return {"error": f"Unsupported risk query_type: {query_type}"}
