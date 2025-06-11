# graph/graph_builder.py

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agents.nodes.hf_intent_node import hf_intent_node
from tools.general_query_tool import general_tool

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

    # 🛠️ Tool node for generalized FastAPI calls
    graph.add_node("query_tool", general_tool)

    # 🔁 Define graph execution
    graph.set_entry_point("router")
    graph.add_edge("router", "query_tool")
    graph.add_edge("query_tool", END)

    return graph.compile()

# 🧪 Test run
if __name__ == "__main__":
    graph = payment_query_graph()
    inputs = {"input": "I lost my card and need to block it"}
    result = graph.invoke(inputs)
    print("\n🎯 Final Result:", result)
