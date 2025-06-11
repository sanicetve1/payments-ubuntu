# agent/nodes/intent_classifier.py
import os
from agents.state import AgentState
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# 🔧 Load your model
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))


# 🧠 Intent classification prompt
INTENT_PROMPT = PromptTemplate.from_template("""
You are an intent classifier for a financial payments agent.

Your job is to classify the user's input into one of the following categories:

- "tool": if the query can be satisfied by a known API tool (like get_payments_by_method, get_flagged_customers)
- "autonomous": if GPT should directly respond (e.g., general analysis, vague/fuzzy queries)
- "unknown": if the intent is unclear

User input: "{user_input}"

Respond with only one word: tool, autonomous, or unknown.
""")


def classify_intent(state: AgentState) -> AgentState:
    """GPT classifies the user intent and updates the state."""
    prompt = INTENT_PROMPT.format(user_input=state.user_input)
    response = llm.predict(prompt).strip().lower()

    if response not in {"tool", "autonomous", "unknown"}:
        response = "unknown"

    state.intent = response
    state.append_step(f"🔍 Intent classified as: {response}")
    return state
