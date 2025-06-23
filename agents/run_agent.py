# run_agent.py
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
#from tools.general_query_tool import general_tool
from tools.api_tools import tools

# 🔐 Load OpenAI API key from .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# 🧠 Initialize LLM with model and key
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=openai_key  # explicitly pass key
)

# 🛠️ Register tools (only api_tools tool for now)
#tools = [tools]

# 🤖 Initialize agent with tool and LLM
agent = initialize_agent(tools, llm, agent_type="openai-tools", verbose=True)

# 🧪 Run an example query
response = agent.run("Give me the names of customers who used card to make payments")

# 📤 Output the final agent response
print("\n===== Agent Response =====")
print(response)
