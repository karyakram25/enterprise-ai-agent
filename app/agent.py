from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama

from state import AgentState
from tools import get_employee_details


# --------------------------------
# Agent Node
# --------------------------------

def agent_node(state: AgentState):

    print("\n--- Agent Node ---")

    messages = state["messages"]

    # --------------------------------
    # First Agent execution
    # --------------------------------

    if not messages:

        print("Creating tool call...")

        ai_message = AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_employee_details",
                    "args": {
                        "employee_id": 101
                    },
                    "id": "call_101",
                    "type": "tool_call"
                }
            ]
        )

        return {
            "messages": [ai_message]
        }

    # --------------------------------
    # Second Agent execution
    # --------------------------------

    print("Tool result received.")

    tool_message = messages[-1]

    llm = ChatOllama(
        model="llama3.2:1b"
    )

    prompt = f"""
The user asked:

{state["user_message"]}

The employee system returned:

{tool_message.content}

Provide a concise and professional response to the user.
Do not mention tools or internal processing.
"""

    response = llm.invoke(prompt)

    print("\nLLM Final Response:")
    print(response.content)

    return {
        "final_response": response.content
    }


# --------------------------------
# Routing Function
# --------------------------------

def route_after_agent(state: AgentState):

    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:

        print("\nRouting → ToolNode")

        return "tools"

    print("\nRouting → END")

    return "end"


# --------------------------------
# Tool Node
# --------------------------------

tool_node = ToolNode(
    [get_employee_details]
)


# --------------------------------
# Create Graph
# --------------------------------

graph = StateGraph(AgentState)


# Nodes
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)


# --------------------------------
# Edges
# --------------------------------

# START → Agent
graph.add_edge(
    START,
    "agent"
)


# Agent → Tool OR END
graph.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        "end": END
    }
)


# Tool → Agent
graph.add_edge(
    "tools",
    "agent"
)


# --------------------------------
# Compile
# --------------------------------

app = graph.compile()


# --------------------------------
# Run
# --------------------------------

result = app.invoke(
    {
        "user_message": "Get the details of employee 101.",
        "messages": [],
        "tool_result": None,
        "final_response": "",
        "needs_tool": False
    }
)


print("\n========== FINAL STATE ==========")
print(result)