import os
from datetime import datetime
from dotenv import load_dotenv
from agents.graph import run_agent_query as graph_agent
from agents.react_agent import run_agent_query as react_agent

# 🔐 Load environment variables
load_dotenv()

LOG_FILE = "agent_test_log.txt"
SUMMARY = []

def log(message: str):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def separator(title=""):
    line = f"\n{'=' * 30} {title} {'=' * 30}\n"
    log(line)

def evaluate_result(result, test_name):
    passed = bool(result.final_output and "error" not in result.final_output.lower())
    status = "✅ PASS" if passed else "❌ FAIL"
    SUMMARY.append(f"{test_name}: {status}")
    return status

def test_graph_tool():
    title = "GRAPH AGENT — Tool Chaining"
    separator(title)
    query = "Show all payments made by card"
    result = graph_agent(query)
    log("Prompt: " + query)
    log("Response:\n" + str(result.final_output))
    log("Steps:\n" + "\n".join(result.intermediate_steps))
    evaluate_result(result, title)

def test_graph_autonomous():
    title = "GRAPH AGENT — Autonomous Reasoning"
    separator(title)
    query = "Why is financial education important for customers?"
    result = graph_agent(query)
    log("Prompt: " + query)
    log("Response:\n" + str(result.final_output))
    log("Steps:\n" + "\n".join(result.intermediate_steps))
    evaluate_result(result, title)

def test_graph_rag():
    title = "GRAPH AGENT — RAG"
    separator(title)
    query = "Explain MAS notice 626 compliance"
    result = graph_agent(query)
    log("Prompt: " + query)
    log("Response:\n" + str(result.final_output))
    log("Steps:\n" + "\n".join(result.intermediate_steps))
    evaluate_result(result, title)

def test_graph_rag_combo():
    title = "GRAPH AGENT — Tool + RAG Hybrid"
    separator(title)
    query = "Get customers who made card payments and explain MAS 626"
    result = graph_agent(query)
    log("Prompt: " + query)
    log("Response:\n" + str(result.final_output))
    log("Steps:\n" + "\n".join(result.intermediate_steps))
    evaluate_result(result, title)

def test_react():
    title = "REACT AGENT — Chain Reasoning"
    separator(title)
    query = "List disputed payments and show customer names"
    result = react_agent(query)
    log("Prompt: " + query)
    log("Response:\n" + str(result.final_output))
    steps = getattr(result, "intermediate_steps", [])
    if steps:
        log("Steps:\n" + "\n".join(steps))
    evaluate_result(result, title)

def run_all_tests():
    start_time = datetime.now().isoformat()
    log(f"🧪 Agent Diagnostic Run — {start_time}\n")

    test_graph_tool()
    test_graph_autonomous()
    test_graph_rag()
    test_graph_rag_combo()
    test_react()

    end_time = datetime.now().isoformat()
    separator("SUMMARY")
    for line in SUMMARY:
        log(line)

    log(f"\n✅ Test run completed at: {end_time}")

if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    run_all_tests()

