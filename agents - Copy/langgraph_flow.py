# agents/langgraph_flow.py

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

from agents.nodes.route_node import route_node
from agents.nodes.fetch_customer_node import customer_node
from agents.nodes.fetch_payments_node import payment_node
from agents.nodes.fetch_risk_node import risk_node

# 🔐 Load .env variables
load_dotenv()

# 🔧 Shared query state
class QueryState(dict):
    pass

# 🧠 LLM initialization (not directly used but loaded for consistency)
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# 🌐 Build the LangGraph flow

def payment_query_graph():
    graph = StateGraph(QueryState)

    graph.add_node("router", route_node)
    graph.add_node("customer_node", customer_node)
    graph.add_node("payment_node", payment_node)
    graph.add_node("risk_node", risk_node)

    # Entry point
    graph.set_entry_point("router")

    # Routing based on query_type
    graph.add_conditional_edges(
        "router",
        lambda state: state.get("query_type"),
        {
            "customers": "customer_node",
            "customer_by_id": "customer_node",
            "customer_payments": "customer_node",
            "payments_by_method": "payment_node",
            "flagged_customers": "risk_node",
            "fallback": END,
        }
    )

    graph.add_edge("customer_node", END)
    graph.add_edge("payment_node", END)
    graph.add_edge("risk_node", END)

    return graph.compile()


# 🧪 For testing
if __name__ == "__main__":
    flow = payment_query_graph()
    result = flow.invoke({"input": "List all customers who used card"}, config=RunnableConfig(tags=["test"]))
    print("\n🎯 Final Result:", result)
