from typing import TypedDict
from langchain_core.messages import AnyMessage


class AgentState(TypedDict):
    user_message: str
    messages: list[AnyMessage]
    tool_result: dict | None
    final_response: str
    needs_tool: bool