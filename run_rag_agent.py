# run_rag_agent.py

from rag_module.rag_mode import set_rag_mode
from agents.state import AgentState
from agents.graph import agent_graph

def run_rag_agent_query(user_input: str, use_full_rag: bool = True):
    set_rag_mode(full=use_full_rag)
    state = AgentState(user_input=user_input)
    raw_result = agent_graph.invoke(state)
    final_state = AgentState(**raw_result)

    print("🤖 Final Output:")
    print(final_state.final_output)
    print("\n📦 Metadata Results:")
    for meta in final_state.tool_result or []:
        print(meta)
    print("\n🧠 Trace:")
    for step in final_state.intermediate_steps:
        print("-", step)

if __name__ == "__main__":
    import sys
    user_input = input("💬 Enter your question: ") if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    run_rag_agent_query(user_input, use_full_rag=False)
