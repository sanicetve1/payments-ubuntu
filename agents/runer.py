# agent/runner.py

from agents.graph import build_graph
from agents.state import AgentState
from agents.memory import init_memory_db, save_state

from dotenv import load_dotenv
load_dotenv()

# ✅ Compile the LangGraph graph once
graph = build_graph()
init_memory_db()

def run_agent_query(user_input: str) -> AgentState:
    """Public function to execute the LangGraph agent with a given user query."""
    state = AgentState(user_input=user_input)
    raw_output = graph.invoke(state)
    final_state = AgentState(**raw_output)
    save_state(final_state)
    return final_state


# Optional: standalone testing via CLI
if __name__ == "__main__":
    user_input = input("💬 Enter your question: ")
    result = run_agent_query(user_input)
    print("\n🤖 Final Output:")
    print(result.final_output)
