
"""Task 2.2: Build a personal AI tutor that remembers recent messages."""

from langchain.chat_models import init_chat_model


llm = init_chat_model("ollama:gemma3:1b", temperature=0.2)

system_message = {
    "role": "system",
    "content": (
        "You are a helpful personal tutor. "
        "Remember information the student shares during the conversation. "
        "Give clear, concise answers in around 3 to 5 sentences."
    ),
}

messages = [system_message]

print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "bye":
        print("Tutor: Goodbye!")
        break

    if user_input.lower() == "/reset":
        # Why: Keep the system message so the tutor does not lose its role.
        messages = [system_message]
        print("Tutor: Memory cleared.")
        continue

    if user_input.lower() == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
        continue

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    response = llm.invoke(messages)

    messages.append({"role": "assistant", "content": response.text})

    print(f"Tutor: {response.text}")
    print(f"       (tokens sent: {response.usage_metadata['input_tokens']})")

    # Why: Limiting history prevents the conversation from growing indefinitely.
    # Why: The system message is preserved while only the latest 8 messages are kept.
    messages = [messages[0]] + messages[1:][-8:]