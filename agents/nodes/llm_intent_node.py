# agents/nodes/llm_intent_node.py

import json
from typing import Dict
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def llm_intent_node(inputs: Dict, config: RunnableConfig) -> Dict:
    user_input = inputs.get("input", "")
    print("\n📥 LLM Intent Node Input:", user_input)

    system_prompt = """
You are a helpful assistant that classifies user input into structured query instructions for a financial chatbot.

Return a JSON object with:
- query_type: One of ['customers', 'customer_by_id', 'payments_by_method', 'customer_payments', 'flagged_customers']
- entity: Optional. Use for customer ID (cus_xxx) or payment method like 'card'.
If nothing is found, respond with {"query_type": "fallback", "entity": null}.
"""

    full_prompt = f"""
{system_prompt}

User Input: {user_input}
"""

    try:
        response = llm.invoke(full_prompt)
        print("🧠 LLM Raw Response:", response.content)
        parsed = json.loads(response.content)
        return parsed
    except Exception as e:
        print("❌ LLM classification failed:", e)
        return {"query_type": "fallback", "entity": None}
