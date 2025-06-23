from agents.state import AgentState
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import json

# 🧠 Load GPT model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🧲 Optional vector match for RAG override
def rag_match(user_input: str, threshold: float = 0.75) -> bool:
    try:
        db = Chroma(
            persist_directory="rag_vectorstore_local",
            embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        )
        results = db.similarity_search_with_score(user_input, k=1)
        if results and results[0][1] >= threshold:
            print(f"🧲 [RAG Match] Score = {results[0][1]:.3f} → triggering RAG")
            return True
        else:
            print(f"🧲 [RAG Match] Score = {results[0][1]:.3f} → below threshold")
    except Exception as e:
        print(f"❌ [RAG Match] Error: {e}")
    return False

# 🧠 Intent classifier with GPT JSON + optional RAG fallback
def classify_intent(state: AgentState) -> AgentState:
    print(f"🧠 [IntentClassifier] Classifying: '{state.user_input}'")

    # Prompt for structured classification
    prompt = (
        "You are an intent classifier for a financial assistant.\n"
        "Return a JSON with:\n"
        "- intent: one of ['tool', 'rag', 'autonomous']\n"
        "- tool_name: if intent is 'tool', choose from known tools\n"
        "- tool_args: optional args like {\"method\": \"card\"}\n\n"
        "Known tools:\n"
        "- get_customers: list all customer records\n"
        "- get_flagged_customers: fetch customers involved in fraud or disputes\n"
        "- get_payments_by_method: list payments filtered by method (e.g. card, cash)\n\n"
        "Examples:\n"
        "- 'List all customers' → get_customers\n"
        "- 'Show card payments' → get_payments_by_method with {\"method\": \"card\"}\n"
        "- 'Get fraudulent customers' → get_flagged_customers\n"
        "- 'What is MAS Notice 626?' → intent: rag\n"
        "- 'Why is financial literacy important?' → intent: autonomous\n\n"
        "Only return JSON. No extra text.\n"
        f"\nUser query: {state.user_input}"
    )

    try:
        raw_response = llm.predict(prompt).strip()
        print(f"📨 [IntentClassifier] Raw LLM output: {raw_response}")
        parsed = json.loads(raw_response)

        state.intent = parsed.get("intent", "autonomous")
        state.tool_name = parsed.get("tool_name")
        state.tool_args = parsed.get("tool_args", {})

    except Exception as e:
        print(f"❌ GPT or JSON parsing error: {e}")
        state.intent = "autonomous"
        state.tool_name = None
        state.tool_args = {}

    # 🔁 Force override to RAG if high vector match
    if rag_match(state.user_input):
        print("🔁 [IntentClassifier] RAG override via high vector match")
        state.intent = "rag"
        state.tool_name = None
        state.tool_args = {}

    # 🚫 DO NOT revert 'rag' just because vector match is low
    # GPT may have seen it's a RAG question (e.g., regulatory/compliance)

    print(f"✅ [IntentClassifier] Final intent: {state.intent}, tool_name: {state.tool_name}, tool_args: {state.tool_args}")
    state.append_step(f"🔍 Intent classified as: {state.intent}")
    return state
