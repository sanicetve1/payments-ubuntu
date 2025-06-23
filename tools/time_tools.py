# tools/time_tools.py
from langchain.tools import Tool
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# 📅 Tool: Get payments from the last 7 days
def fetch_recent_payments(days: int = 7):
    cutoff = datetime.utcnow() - timedelta(days=days)
    timestamp = int(cutoff.timestamp())
    response = requests.get(f"{BASE_URL}/payments/recent", params={"after": timestamp})
    return response.json()

time_tools = [
    Tool.from_function(
        name="get_recent_payments",
        description="Get all payments made in the last 7 days or N days",
        func=fetch_recent_payments
    )
]
