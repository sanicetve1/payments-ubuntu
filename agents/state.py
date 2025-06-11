# agent/state.py

from typing import Optional, List, Any
from pydantic import BaseModel, Field
import json
import uuid
from datetime import datetime


class AgentState(BaseModel):
    """
    Defines the LangGraph agent state object.
    Tracks reasoning, user input, tool decisions, memory, and final output.
    """

    user_input: str                            # Raw user query
    intent: Optional[str] = None               # Detected intent: 'tool', 'autonomous', etc.
    tool_name: Optional[str] = None            # Chosen tool (if applicable)
    tool_args: Optional[dict] = None           # Parameters passed to tool
    tool_result: Optional[Any] = None          # Output returned from tool
    gpt_response: Optional[str] = None         # Raw response from GPT if used freely
    final_output: Optional[str] = None         # What the agent sends back to the user
    intermediate_steps: List[str] = Field(default_factory=list)  # Node-by-node trace

    # Persistent memory and metadata
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    history: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def append_step(self, step: str):
        self.intermediate_steps.append(step)

    def add_to_history(self, message: str):
        self.history.append(message)

    def serialize(self) -> str:
        """Convert to JSON string for DB storage."""
        return self.json()

    @classmethod
    def deserialize(cls, data: str) -> "AgentState":
        """Rehydrate from DB JSON string."""
        return cls.parse_raw(data)

    def summary(self) -> str:
        """Short representation for logs or dashboards."""
        return f"[{self.timestamp}] ({self.intent}) {self.user_input} → {self.final_output}"
