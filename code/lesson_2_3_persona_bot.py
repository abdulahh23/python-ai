
"""Task 2.3: Create a bakery chatbot with different personas and real business facts."""

from langchain.chat_models import init_chat_model


# Business information used by the AI assistant.
facts = {
    "name": "Sweet Crumbs Bakery",
    "business_type": "Bakery",
    "city": "Lahore",
    "customers": "Students, families, and dessert lovers",
    "opening_hours": "9 AM to 9 PM",
    "delivery": "Available in Lahore",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
        "donut": 200,
        "cookies": 150,
    },
}

# Each persona changes the way the AI communicates.
personas = {
    "friendly": "You are warm, cheerful, and use simple, welcoming language.",
    "formal": "You are professional, polite, and use formal language.",
    "sales": "You are enthusiastic and always suggest one extra menu item to buy.",
}

config = {
    "model": "ollama:gemma3:1b",
    "temperature": 0.2,
    "memory_size": 8,
}

llm = init_chat_model(
    config["model"],
    temperature=config["temperature"],
)


def build_system_message(persona_name):
    """Build the system message using bakery facts and the selected persona."""

    # Why: Using the actual dictionary keeps the AI's business information consistent.
    return {
        "role": "system",
        "content": (
            f"You are the customer service assistant for {facts['name']}.\n"
            f"Business facts: {facts}\n"
            f"Your personality: {personas.get(persona_name, personas['friendly'])}\n"
            "Only use these facts when answering questions about the business. "
            "Never invent products, prices, opening hours, or services. "
            "If information is missing, politely say you do not know."
        ),
    }


current_persona = "friendly"
messages = [build_system_message(current_persona)]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, bye")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "bye":
        print("Bot: Goodbye!")
        break

    if user_input.lower().startswith("/persona"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            print("Bot: Please provide a persona name.")
            continue

        requested_persona = parts[1].lower()

        # Why: .get() provides a safe default instead of raising a KeyError.
        selected_persona = personas.get(requested_persona, personas["friendly"])

        if requested_persona in personas:
            current_persona = requested_persona
            print(f"Bot: Style changed to: {selected_persona}")
        else:
            current_persona = "friendly"
            print("Bot: Unknown persona. Using the friendly style.")

        # Why: Updating the system message changes the AI's personality immediately.
        messages[0]["content"] = build_system_message(current_persona)["content"]
        continue

    if user_input.lower().startswith("/price"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            print("Bot: Please provide a menu item.")
            continue

        item = parts[1].strip().lower()
        price = facts["prices"].get(item)

        # Why: Dictionary lookup gives accurate prices without an AI-generated guess.
        if price is not None:
            print(f"Bot: {item.title()} costs {price} PKR.")
        else:
            print(f"Bot: Sorry, {item.title()} is not on our menu.")
        continue

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    response = llm.invoke(messages)

    messages.append({"role": "assistant", "content": response.text})

    print(f"Bot: {response.text}")

    # Keep the system message and the latest conversation messages.
    messages = [messages[0]] + messages[1:][-config["memory_size"]:]