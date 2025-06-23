from agents.state import AgentState
from rag_module.rag_vectorstore import secure_rag_query, full_rag_query
from langchain.chat_models import ChatOpenAI
import os

llm = ChatOpenAI(model="gpt-4", temperature=0)

def run_rag_node_secure(state: AgentState) -> AgentState:
    results = secure_rag_query(state.user_input)
    state.tool_result = results  # ✅ Store metadata
    state.final_output = f"Retrieved {len(results)} records (metadata only)."
    state.append_step("🔍 RAG node executed in SECURE mode.")
    return state

def run_rag_node_full(state: AgentState) -> AgentState:
    chunks = full_rag_query(state.user_input)
    context = "\n".join(chunks[:5])
    prompt = f"Context:\n{context}\n\nQuestion: {state.user_input}"
    response = llm.predict(prompt).strip()
    state.final_output = response
    state.append_step("🧠 RAG node executed in FULL GPT mode.")
    return state
