# agents/nodes/chain_executor_node.py

from agents.state import AgentState
from tools.api_tools import fetch_customers_by_ids

def chain_executor_node(state: AgentState) -> AgentState:
    print("🔁 [chain_executor_node] Starting tool chaining logic...")

    # Safety check: Ensure previous tool_result is a list
    if not state.tool_result:
        print("⚠️ [chain_executor_node] No tool_result found.")
        state.append_step("⚠️ No previous tool result available.")
        return state

    if not isinstance(state.tool_result, list):
        print(f"❌ [chain_executor_node] Unexpected tool_result type: {type(state.tool_result)}")
        state.append_step("❌ Previous tool result is not a list. Skipping chaining.")
        return state

    print(f"🔍 [chain_executor_node] Received {len(state.tool_result)} items in tool_result.")

    # Step 1: Extract customer_ids from tool_result
    customer_ids = list({
        item.get("customer_id") for item in state.tool_result
        if isinstance(item, dict) and item.get("customer_id")
    })

    print(f"🧮 [chain_executor_node] Extracted customer_ids: {customer_ids}")

    if not customer_ids:
        print("⚠️ [chain_executor_node] No customer_ids found in tool_result.")
        state.append_step("⚠️ No customer_ids found — skipping chaining.")
        return state

    # Step 2: Fetch customer details using the extracted IDs
    print(f"📡 [chain_executor_node] Calling fetch_customers_by_ids with {len(customer_ids)} IDs...")
    try:
        customers = fetch_customers_by_ids(customer_ids)
        print(f"✅ [chain_executor_node] Fetched {len(customers)} customer records.")
    except Exception as e:
        print(f"❌ [chain_executor_node] Failed to fetch customer details: {e}")
        state.append_step(f"❌ Error during customer chaining: {e}")
        return state

    # Step 3: Update state
    state.tool_result = customers
    state.final_output = "\n".join(
        f"{c.get('name', 'Unknown')} (ID: {c.get('id', '-')})" for c in customers
    )
    state.append_step("🔗 Chained tool: fetched customer details from previous payment result.")

    return state
