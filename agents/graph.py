import streamlit as st
import time
from langgraph.graph import StateGraph
from agents.state import AgentState
from agents.nodes.intent_classifier import classify_intent
from agents.nodes.autonomous_gpt_node import run_autonomous_gpt
from agents.nodes.chain_executor_node import chain_executor_node
from agents.nodes.thinking_node import thinking_node
from tools.api_tools import (
    fetch_customers,
    fetch_payments_by_method,
    fetch_flagged_customers,
)
from tools.rag_tool import query_rag_tool

# === Format utility ===
def format_preview(items: list, label: str) -> str:
    if not items:
        return f"No {label} records found."
    preview_lines = [f"{i+1}. {item.get('name', item.get('id', 'Unknown'))}" for i, item in enumerate(items[:3])]
    preview_text = "\n".join(preview_lines)
    return f"Found {len(items)} {label} records.\nTop results:\n{preview_text}"

# === Tool Nodes ===
def get_customers_node(state: AgentState) -> AgentState:
    print("🔧 [get_customers_node] Executing tool: fetch_customers")
    with st.spinner("Fetching customers..."):
        time.sleep(1)
        state.tool_result = fetch_customers()
    print(f"📦 [get_customers_node] Tool result: {state.tool_result}")
    state.final_output = format_preview(state.tool_result, "customer")
    state.routing_decision = "final_formatter_node"
    state.append_step("✅ Retrieved customers")
    return state

def get_payments_by_method_node(state: AgentState) -> AgentState:
    print("🔧 [get_payments_by_method_node] Executing tool: fetch_payments_by_method")
    method = state.tool_args.get("method")
    print(f"🔍 [get_payments_by_method_node] Method argument: {method}")
    with st.spinner(f"Fetching payments with method: {method}..."):
        time.sleep(1)
        state.tool_result = fetch_payments_by_method(method)
    print(f"📦 [get_payments_by_method_node] Tool result: {state.tool_result}")
    state.append_step(f"✅ Retrieved payments with method: {method}")
    return state

def get_flagged_customers_node(state: AgentState) -> AgentState:
    print("🔧 [get_flagged_customers_node] Executing tool: fetch_flagged_customers")
    with st.spinner("Fetching flagged customers..."):
        time.sleep(1)
        state.tool_result = fetch_flagged_customers()
    print(f"📦 [get_flagged_customers_node] Tool result: {state.tool_result}")
    state.final_output = format_preview(state.tool_result, "flagged customer")
    state.routing_decision = "final_formatter_node"
    state.append_step("✅ Retrieved flagged customers")
    return state

# === Non-tool Nodes ===
def rag_node(state: AgentState) -> AgentState:
    print("📄 [rag_node] Running RAG vector search")
    result = query_rag_tool(state.user_input)
    print(f"📄 [rag_node] RAG result: {result}")
    state.final_output = result
    state.append_step("📄 RAG result fetched")
    return state

def autonomous_node(state: AgentState) -> AgentState:
    print("🧠 [autonomous_node] Executing GPT autonomous reasoning")
    return run_autonomous_gpt(state)

def decision_router_node(state: AgentState) -> AgentState:
    print("🔁 [decision_router_node] Evaluating whether chaining is needed...")
    if state.tool_result and isinstance(state.tool_result, list):
        if any("customer_id" in item for item in state.tool_result if isinstance(item, dict)):
            print("➡️ Found customer_id → setting route to 'chain_executor_node'")
            state.routing_decision = "chain_executor_node"
        else:
            print("✅ No customer_id found → setting route to 'final_formatter_node'")
            state.routing_decision = "final_formatter_node"
    else:
        print("⚠️ tool_result not a list or empty → setting route to 'final_formatter_node'")
        state.routing_decision = "final_formatter_node"
    state.append_step(f"🔁 decision_router chose: {state.routing_decision}")
    return state

def decision_router_fn(state: AgentState) -> str:
    print(f"➡️ [decision_router_fn] Routing to: {state.routing_decision}")
    return state.routing_decision or "final_formatter_node"

def final_formatter_node(state: AgentState) -> AgentState:
    print("🎯 [final_formatter_node] Formatting final output...")
    if isinstance(state.tool_result, list):
        preview = "\n".join(
            f"{i+1}. {r.get('name', r.get('id', 'Unknown'))} ({r.get('country', 'N/A')})"
            for i, r in enumerate(state.tool_result[:3])
        )
        state.final_output = f"Top Customers:\n{preview}"
    elif isinstance(state.tool_result, dict):
        state.final_output = str(state.tool_result)
    else:
        state.final_output = "✅ No detailed result to format."

    thought_lines = [step for step in state.intermediate_steps if step.startswith("🧠 Thought:")]
    if thought_lines:
        last_thought = thought_lines[-1].replace("🧠 Thought: ", "💡 Suggested Action: ")
        state.final_output += f"\n\n{last_thought}"

    state.append_step("✅ Final output formatted")
    return state

def intent_branch(state: AgentState) -> str:
    print(f"🧭 [intent_branch] Intent classified as: {state.intent}")
    return state.intent

def tool_router(state: AgentState) -> dict:
    tool = state.tool_name
    print(f"🔀 [tool_router] Routing to specific tool node: {tool}")
    if tool in {"get_customers", "get_payments_by_method", "get_flagged_customers"}:
        return {"next": tool}
    print("⚠️ Unknown tool_name. Routing to autonomous_node")
    return {"next": "autonomous_node"}

# === Graph ===
print("🧠 [graph] Initializing LangGraph workflow")
workflow = StateGraph(AgentState)

workflow.add_node("intent_router", classify_intent)
workflow.add_node("tool_router", tool_router)
workflow.add_node("get_customers", get_customers_node)
workflow.add_node("get_payments_by_method", get_payments_by_method_node)
workflow.add_node("get_flagged_customers", get_flagged_customers_node)
workflow.add_node("rag_node", rag_node)
workflow.add_node("autonomous_node", autonomous_node)
workflow.add_node("decision_router_node", decision_router_node)
workflow.add_node("chain_executor_node", chain_executor_node)
workflow.add_node("final_formatter_node", final_formatter_node)
workflow.add_node("thinking_node", thinking_node)

workflow.set_entry_point("intent_router")

workflow.add_conditional_edges("intent_router", intent_branch, {
    "tool": "tool_router",
    "rag": "rag_node",
    "autonomous": "autonomous_node"
})

workflow.add_conditional_edges("tool_router", lambda s: tool_router(s)["next"], {
    "get_customers": "get_customers",
    "get_payments_by_method": "get_payments_by_method",
    "get_flagged_customers": "get_flagged_customers",
    "autonomous_node": "autonomous_node"
})

workflow.add_edge("get_customers", "thinking_node")
workflow.add_edge("get_flagged_customers", "thinking_node")
workflow.add_edge("get_payments_by_method", "thinking_node")
workflow.add_edge("chain_executor_node", "thinking_node")
workflow.add_edge("thinking_node", "decision_router_node")

workflow.add_conditional_edges("decision_router_node", decision_router_fn, {
    "chain_executor_node": "chain_executor_node",
    "final_formatter_node": "final_formatter_node"
})

workflow.set_finish_point("final_formatter_node")
workflow.set_finish_point("rag_node")
workflow.set_finish_point("autonomous_node")

def run_agent_query(user_input: str):
    print(f"\n🟢 [run_agent_query] Received: '{user_input}'")
    initial_state = AgentState(user_input=user_input)
    output_dict = agent_graph.invoke(initial_state)
    print("📦 [run_agent_query] Raw state keys returned:")
    for key, value in output_dict.items():
        summary = str(value)
        if isinstance(value, list):
            summary = f"{len(value)} items"
        elif isinstance(value, str) and len(value) > 100:
            summary = value[:100] + "..."
        print(f"   - {key}: {summary}")
    final_state = AgentState(**output_dict)
    print("✅ [run_agent_query] Final output:", final_state.final_output)
    return final_state

agent_graph = workflow.compile()

def build_autonomous_agent_graph():
    print("✅ [graph] Building structured LangGraph agent...")
    return agent_graph
