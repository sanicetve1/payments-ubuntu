# react_agent.py

from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from tools.api_tools import tools

# 🧠 Load GPT model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🤖 ReAct-style agent using tool descriptions and reasoning loop
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="react",
    verbose=True,
    handle_parsing_errors=True
)

# 🚀 Entry point to run the ReAct agent
from types import SimpleNamespace

def run_agent_query(user_input: str):
    print(f"\n🚀 [ReAct Agent] Processing query: {user_input}\n")
    try:
        response = agent.invoke(user_input)
        print("✅ [ReAct Agent] Response:", response)

        # Wrap string in result-like object for compatibility with UI
        return SimpleNamespace(
            final_output=response,
            tool_result=[],
            intermediate_steps=["✅ ReAct agent executed."],
            history=[user_input]
        )

    except Exception as e:
        print("❌ [ReAct Agent] Error:", e)
        return SimpleNamespace(
            final_output=f"ReAct agent failed: {e}",
            tool_result=[],
            intermediate_steps=[f"❌ ReAct error: {e}"],
            history=[user_input]
        )

