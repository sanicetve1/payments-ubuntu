# test_backend_call.py

import sys
import os

# ✅ Add the path to the project root (where agent/ lives)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.runer import run_agent_query

backend_input = "Do we have many customers in Asia with fraud history?"
result_state = run_agent_query(backend_input)

print("==== Final Output ====")
print(result_state.final_output)
