# AgentUI.py

import os
import sys
import types
import torch
import traceback
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# --- Fix Torch ImportError for Chroma on Windows ---
sys.modules["torch.classes"] = types.ModuleType("torch.classes")

# --- Load Environment Variables ---
load_dotenv(override=True)

if os.getenv("OPENAI_API_KEY"):
    print("🔐 OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10] + "...")

# Fix path to enable agent import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print("📂 Working directory:", os.getcwd())

# --- Import both agents ---
from agents.graph import run_agent_query as run_langgraph_agent
from agents.react_agent import run_agent_query as run_react_agent

# --- Smart Router Function ---
def run_agent_query(user_input: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] 🔍 Received query: {user_input}")

    try:
        if user_input.lower().strip().startswith("react:"):
            clean_input = user_input[6:].strip()
            print("🧠 Forced ReAct agent via prefix")
            result = run_react_agent(clean_input)
            print("✅ ReAct agent response complete")
        else:
            print("🧱 Routed to LangGraph agent")
            result = run_langgraph_agent(user_input)
            print("✅ LangGraph agent response complete")
    except Exception as e:
        print("❌ Agent failed:", e)
        traceback.print_exc()
        result = type("FallbackResult", (object,), {
            "final_output": "Something went wrong. Please try again.",
            "tool_result": [],
            "intermediate_steps": [f"Error: {str(e)}"],
            "history": []
        })()
    return result

# ✅ Streamlit UI Setup
st.set_page_config(page_title="Payments Agent", layout="wide")
st.title("💳 Financial Assistant")

# --- Query Input ---
user_query = st.text_input("Ask a question about payments, customers, or regulations:", key="user_query")

# --- Chat History Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Trigger Button ---
if st.button("Ask Agent") and user_query:
    result = run_agent_query(user_query)

    if result.final_output:
        st.success(result.final_output)
    else:
        st.warning("🤔 No output returned by the agent.")

    # Show raw tool_result metadata if available
    if result.tool_result:
        st.markdown("### 🧾 Retrieved Records (Metadata)")
        for i, record in enumerate(result.tool_result, 1):
            st.markdown(f"**Record {i}:**")
            st.json(record)

    # Agent trace steps
    with st.expander("🧠 Agent Trace (Steps)", expanded=False):
        for step in result.intermediate_steps:
            st.markdown(f"- {step}")

    # Save conversation history
    if result.history:
        st.session_state.chat_history.extend(result.history)

# --- Sidebar for Past Conversation ---
with st.sidebar.expander("🕘 Past Conversations", expanded=True):
    if st.session_state.chat_history:
        for i, step in enumerate(st.session_state.chat_history):
            st.markdown(f"**{i+1}.** {step}")
    else:
        st.markdown("_No past conversation yet._")
