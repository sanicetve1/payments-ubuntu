#from agents.graph import build_autonomous_agent_graph
from agents.graph import agent_graph
from agents.state import AgentState
from agents.memory import init_memory_db, save_state
from dotenv import load_dotenv
load_dotenv()

#graph = build_autonomous_agent_graph()
init_memory_db()

def run_agent_query(user_input: str) -> AgentState:
    print(f"\n🚀 Running agent query: {user_input}")
    state = AgentState(user_input=user_input)

    result = agent_graph.invoke(state)
    print("🔍 Raw result from LangGraph:", result)

    # ✅ Safely reconstruct AgentState from returned dict
    final_state = AgentState(**result)

    print("✅ final_state type:", type(final_state))
    assert isinstance(final_state, AgentState), f"❌ Expected AgentState, got {type(final_state)}"

    save_state(final_state)
    print("💾 Agent state saved to memory.")
    return final_state

if __name__ == "__main__":
    user_input = input("💬 Enter your question: ")
    result = run_agent_query(user_input)
    print("\n🤖 Final Output:")
    print(result.final_output)
