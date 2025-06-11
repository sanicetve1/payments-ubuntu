#graph/graph_builder.py

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agents.nodes.hf_intent_node import hf_intent_node
from tools.general_query_tool import (
    get_customers_tool,
    get_customer_by_id_tool,
    get_payments_by_method_tool,
    get_customer_payments_tool,
    get_flagged_customers_tool
)

# 🔐 Load environment variables
load_dotenv()

# 🗺️ Define state wrapper
class QueryState(dict):
    pass

# 🔧 Build LangGraph using HF classifier intent routing
def payment_query_graph():
    graph = StateGraph(QueryState)

    # 🧠 Intent classification using HF
    graph.add_node("router", hf_intent_node)

    # 🛠️ Add tool nodes
    graph.add_node("get_customers", get_customers_tool)
    graph.add_node("get_customer_by_id", get_customer_by_id_tool)
    graph.add_node("get_payments_by_method", get_payments_by_method_tool)
    graph.add_node("get_customer_payments", get_customer_payments_tool)
    graph.add_node("get_flagged_customers", get_flagged_customers_tool)

    # 🔁 Entry point
    graph.set_entry_point("router")

    # ➰ Conditional routing based on query_type
    graph.add_conditional_edges(
        "router",
        lambda state: state.get("query_type"),
        {
            "customers": "get_customers",
            "customer_by_id": "get_customer_by_id",
            "payments_by_method": "get_payments_by_method",
            "customer_payments": "get_customer_payments",
            "flagged_customers": "get_flagged_customers",
        }
    )

    # 🛑 End after each tool completes
    graph.add_edge("get_customers", END)
    graph.add_edge("get_customer_by_id", END)
    graph.add_edge("get_payments_by_method", END)
    graph.add_edge("get_customer_payments", END)
    graph.add_edge("get_flagged_customers", END)

    return graph.compile()

# 🧪 Test run
if __name__ == "__main__":
    graph = payment_query_graph()
    inputs = {"input": "Show me all customers who used card"}
    result = graph.invoke(inputs)
    print("\n🎯 Final Result:", result)

# 🛠️ Function to build and return a compiled LangGraph workflow
def payment_query_graph():
    graph = StateGraph(QueryState)

    # 🔁 Use LLM intent classifier as the router node
    graph.add_node("router", llm_intent_node)

    # 🧰 Use general tool node to handle all queries
    graph.add_node("query_tool", general_tool)

    # 🔁 Define routing logic
    graph.set_entry_point("router")
    graph.add_edge("router", "query_tool")
    graph.add_edge("query_tool", END)

    return graph.compile()

# 🧪 For test runs
if __name__ == "__main__":
    graph = payment_query_graph()
    result = graph.invoke({"input": "show me all customers who paid by card"})
    print("\n🎯 Final Result:", result)
