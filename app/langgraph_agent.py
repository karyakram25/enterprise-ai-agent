from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_ollama import ChatOllama
from pydantic import BaseModel

llm = ChatOllama(
    model="llama3.2:1b"
)

class IntentClassification(BaseModel):
    intent: Literal["greeting", "general"]

structured_llm = llm.with_structured_output(IntentClassification)

# 1. Define the information our graph will carry
class State(TypedDict):
    user_message: str
    is_valid: bool
    intent: str
    response: str


# 2. Validate the message
def validate_message(state: State):
    print("Validating message:", state["user_message"])

    if not state["user_message"]:
        return {
            "is_valid": False
        }

    return {
        "is_valid": True
    }


# 3. Analyze the message
def analyze_message(state: State):
    print("Analyzing message:", state["user_message"])

    response = structured_llm.invoke(
        f"""
        Classify this user message.

        If the user is greeting, return greeting.

        If the user is asking for help or anything else, return general.

        User message:
        {state["user_message"]}
        """
    )

    print("Structured LLM response:", response)

    return {
        "intent": response.intent
    }

# 4. Decide whether message is valid
def decide_next_step(state: State):
    if state["is_valid"]:
        return "process"

    return "end"


# 5. Decide based on intent
def route_by_intent(state: State):
    if state["intent"] == "greeting":
        return "greeting"

    return "general"


# 6. Greeting node
def greeting_response(state: State):
    print("Handling greeting")

    return {
        "response": "Hello! How can I help you?"
    }


# 7. General request node
def general_response(state: State):
    print("Handling general request")

    return {
        "response": "I will help you with your request."
    }


# 8. Create graph
graph = StateGraph(State)


# 9. Add nodes
graph.add_node("validator", validate_message)
graph.add_node("analyzer", analyze_message)
graph.add_node("greeting_response", greeting_response)
graph.add_node("general_response", general_response)


# 10. Define workflow
graph.add_edge(START, "validator")

graph.add_conditional_edges(
    "validator",
    decide_next_step,
    {
        "process": "analyzer",
        "end": END
    }
)

graph.add_conditional_edges(
    "analyzer",
    route_by_intent,
    {
        "greeting": "greeting_response",
        "general": "general_response"
    }
)

graph.add_edge("greeting_response", END)
graph.add_edge("general_response", END)


# 11. Compile graph
app = graph.compile()


# 12. Run graph
result = app.invoke({
    "user_message": "Good morning, I wanted to say hi.",
    "is_valid": False,
    "intent": "",
    "response":""
})


# 13. Print result
print(result)