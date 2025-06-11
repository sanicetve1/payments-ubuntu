# agent/nodes/autonomous_gpt_node.py

from agents.state import AgentState
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize GPT model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Optional: Prompt template to keep tone professional
AUTONOMOUS_PROMPT = PromptTemplate.from_template("""
You are a helpful assistant for a financial payments platform.

Context:
- The user is asking a question that is not directly solvable with a tool.
- You should provide a thoughtful, well-reasoned response using common sense and your knowledge of payment systems.

Conversation history (if any):
{history}

Current user input:
{user_input}

Respond clearly and helpfully.
""")

def run_autonomous_gpt(state: AgentState) -> AgentState:
    """Handles fuzzy or broad user questions with GPT."""
    prompt = AUTONOMOUS_PROMPT.format(
        user_input=state.user_input,
        history="\n".join(state.history[-5:])  # optional: only last 5 entries
    )
    response = llm.predict(prompt).strip()

    state.gpt_response = response
    state.final_output = response
    state.append_step("🧠 GPT autonomously responded")
    state.add_to_history(f"User: {state.user_input}\nGPT: {response}")
    return state
