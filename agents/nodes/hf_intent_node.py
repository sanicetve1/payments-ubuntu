# agents/nodes/hf_intent_node.py

from transformers import pipeline
from langchain_core.runnables import RunnableConfig
from typing import Dict

# Load the pretrained classifier
classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-banking77")

# Map HF labels to your system's query_type and entity mappings
label_to_query_type = {
    "card_block": {"query_type": "flagged_customers", "entity": None},
    "card_payment_wrong_exchange_rate": {"query_type": "payments_by_method", "entity": "card"},
    "transactions": {"query_type": "customer_payments", "entity": "cus_Sample"},
    "balance": {"query_type": "customers", "entity": None},
    # Add more mappings as needed
}

def hf_intent_node(inputs: Dict, config: RunnableConfig) -> Dict:
    user_input = inputs.get("input", "")
    print("\n📥 HF Intent Node Input:", user_input)

    try:
        prediction = classifier(user_input, top_k=1)[0]
        label = prediction["label"]
        print("🏷️ Predicted Label:", label)

        if label in label_to_query_type:
            return label_to_query_type[label]
        else:
            return {"query_type": "fallback", "entity": None}

    except Exception as e:
        print("❌ HF classifier failed:", e)
        return {"query_type": "fallback", "entity": None}
