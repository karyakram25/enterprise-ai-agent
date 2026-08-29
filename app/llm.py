from langchain_ollama import ChatOllama
from tools import get_employee_details


llm = ChatOllama(
    model="llama3.2:1b"
)


# Step 1: User request
user_message = "Get the details of employee 101."


# Step 2: Simulated tool call
tool_request = {
    "name": "get_employee_details",
    "parameters": {
        "employee_id": 101
    }
}


# Step 3: Execute the tool
tool_result = get_employee_details.invoke(
    tool_request["parameters"]
)

print("Tool Result:")
print(tool_result)


# Step 4: Send tool result back to LLM
final_response = llm.invoke(
    f"""
The user asked:

{user_message}

The employee system returned this information:

{tool_result}

Using this information, provide a concise answer to the user.
"""
)


print("\nFinal Response:")
print(final_response.content)