# agent/graph.py

from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
import os
from agents.state import AgentState
from agents.nodes.intent_classifier import classify_intent
from agents.nodes.autonomous_gpt_node import run_autonomous_gpt
from tools.api_tools import tools
from langchain.agents import initialize_agent
from dotenv import load_dotenv
load_dotenv()


# 🧠 Setup LLM for tool-using agent
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

# 🛠️ Initialize LangChain agent with your FastAPI tools
tool_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="openai-tools",
    verbose=True
)


# 🔁 Tool execution wrapper
def run_tool_node(state: AgentState) -> AgentState:
    response = tool_agent.run(state.user_input)
    state.tool_result = response
    state.final_output = response
    state.append_step("🔧 Tool agent executed the request")
    state.add_to_history(f"User: {state.user_input}\nTool: {response}")
    return state


# 🚨 Fallback for unrecognized input
def fallback_handler(state: AgentState) -> AgentState:
    fallback = "I'm not sure how to handle that. Could you rephrase your request?"
    state.final_output = fallback
    state.append_step("❓ Unknown intent - fallback triggered")
    state.add_to_history(f"User: {state.user_input}\nAgent: {fallback}")
    return state


# 🔁 Build the LangGraph
def build_graph():
    workflow = StateGraph(AgentState)

    # Add core processing nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("run_tool_node", run_tool_node)
    workflow.add_node("run_gpt_node", run_autonomous_gpt)
    workflow.add_node("fallback_node", fallback_handler)

    # Start: user input → intent classification
    workflow.set_entry_point("classify_intent")

    # Routing logic after classification
    workflow.add_conditional_edges(
        "classify_intent",
        lambda state: state.intent,
        {
            "tool": "run_tool_node",
            "autonomous": "run_gpt_node",
            "unknown": "fallback_node"
        }
    )

    # Each handler ends the graph
    workflow.set_finish_point("run_tool_node")
    workflow.set_finish_point("run_gpt_node")
    workflow.set_finish_point("fallback_node")

    return workflow.compile()
