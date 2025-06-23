# agents/nodes/thinking_node.py

from agents.state import AgentState
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# ✅ Initialize the same GPT model as other nodes
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🧠 Reasoning prompt — simple, universal
THINK_PROMPT = PromptTemplate.from_template("""
You are an internal reasoning engine for a financial assistant.

Context:
- The user said: "{user_input}"
- The tool returned the following result (trimmed):

{tool_result}

What should be done next? Return a concise "Thought:".
""")

def thinking_node(state: AgentState) -> AgentState:
    print("🧠 [thinking_node] Reflecting on previous step...")

    try:
        prompt_text = THINK_PROMPT.format(
            user_input=state.user_input,
            tool_result=str(state.tool_result)[:1000]  # truncate to avoid token overflow
        )

        thought = llm.predict(prompt_text).strip()
        print(f"🧠 [thinking_node] Thought: {thought}")

        state.append_step("🧠 Thought: " + thought)

        # optionally, you can also log it in a field like state.gpt_response_thought if needed
    except Exception as e:
        print(f"⚠️ [thinking_node] GPT failed: {e}")
        state.append_step("⚠️ Thought generation failed")

    return state
