# run_agent.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOpenAI
from tools.api_tools import tools

# 🔐 Explicitly retrieve API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment or .env file.")

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    openai_api_key=api_key
)

agent = initialize_agent(tools, llm, agent_type="openai-tools", verbose=True)

response = agent.run("payments made in the last 1 day")
print("\n===== Agent Response =====")
print(response)
