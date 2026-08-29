from ollama import chat

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAI:", response.message.content)