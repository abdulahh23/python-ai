
"""AI Content Studio for Sweet Crumbs Bakery in Lahore.

This studio generates bakery menu descriptions, streams social media posts,
answers prices from verified business data, and chats with customers using
conversation memory.
"""

from langchain.chat_models import init_chat_model


# Configuration for the models and conversation memory.
config = {
    "model": "ollama:gemma3:1b",
    "max_messages": 8,
}

# Verified business information used to ground the AI's answers.
facts = {
    "name": "Sweet Crumbs Bakery",
    "business_type": "Bakery",
    "city": "Lahore",
    "hours": "9 AM to 10 PM",
    "delivery": "Available in Lahore",
    "delivery_fee": "200 PKR",
    "free_delivery": "Free delivery on orders of 3,000 PKR or more",
    "customers": "Students, families, and dessert lovers",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
        "mango tart": 0,
    },
}

# Different writing styles for social media content.
tones = {
    "fun": "Playful and full of energy. Use short, exciting sentences.",
    "premium": "Elegant and calm, focused on quality and craftsmanship.",
    "urgent": "Create a sense of urgency and encourage customers to order today.",
}

# Why: Separate models let us prioritize accuracy for chat and creativity for marketing.
precise_model = init_chat_model(
    config["model"],
    temperature=0.2,
)

creative_model = init_chat_model(
    config["model"],
    temperature=0.8,
)

# Why: Building the system message from facts keeps business information consistent.
system_message = {
    "role": "system",
    "content": (
        f"You are the customer service assistant for {facts['name']}.\n"
        f"Here are the verified business facts: {facts}\n"
        "Only use these facts when answering questions about the business. "
        "Never invent products, prices, opening hours, or services. "
        "If you do not know something, clearly say that you do not have "
        "that information."
    ),
}

messages = [system_message]

# Session counters.
chat_answers = 0
menu_descriptions = 0
posts = 0
price_answers = 0
total_tokens = 0
total_seconds = 0.0


# Application header.
print("=" * 50)
print("   Sweet Crumbs AI Content Studio")
print("=" * 50)
print("Commands: /menu, /post fun|premium|urgent, /price <item>, /reset, bye")


while True:
    user_input = input("You: ").strip()

    # Why: Empty input should not trigger an unnecessary AI request.
    if not user_input:
        print("Studio: Please enter a command or ask a question.")
        continue

    command = user_input.lower()

    # Exit the studio.
    if command == "bye":
        print("Studio: Goodbye!")
        break

    # Reset conversation memory while keeping the system message.
    elif command == "/reset":
        messages = [system_message]
        print("Studio: Chat memory cleared.")

    # Generate descriptions for all priced menu items.
    elif command == "/menu":
        results = []

        for name, price in facts["prices"].items():

            # Why: A zero price means the product is coming soon, not available to order.
            if price == 0:
                print(f"Studio: Skipping {name} (coming soon)")
                continue

            prompt = (
                f"Write one attractive sentence describing {name} "
                f"for {facts['name']} in {facts['city']}. "
                f"The price is {price} PKR. "
                "Keep it short and suitable for a bakery menu."
            )

            response = creative_model.invoke(prompt)

            results.append(
                {
                    "item": name,
                    "price": price,
                    "text": response.text,
                }
            )

            menu_descriptions += 1
            total_tokens += response.usage_metadata.get("total_tokens", 0)
            total_seconds += (
                response.response_metadata.get("total_duration", 0)
                / 1_000_000_000
            )

        print("-" * 50)

        for number, product in enumerate(results, start=1):
            print(f"{number}. {product['item'].title()} ({product['price']:,} PKR)")
            print(f"   {product['text']}")

        print("-" * 50)

    # Generate a streamed social media post.
    elif command.startswith("/post"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            print("Studio: Please provide a tone: fun, premium, or urgent.")
            continue

        requested_tone = parts[1].strip().lower()

        # Why: .get() provides a default tone if the requested tone is unknown.
        selected_tone = tones.get(requested_tone, tones["fun"])

        if requested_tone not in tones:
            print("Studio: Unknown tone. Using the fun tone.")

        post_messages = [
            {
                "role": "system",
                "content": (
                    f"You write social media posts for {facts['name']}. "
                    f"Business facts: {facts}. "
                    f"Writing tone: {selected_tone} "
                    "Only use the provided facts. Do not invent offers or prices. "
                    "Write a short, engaging Instagram post."
                ),
            },
            {
                "role": "user",
                "content": "Write an Instagram post for our bakery.",
            },
        ]

        print(f"Studio ({selected_tone}):")

        stream_tokens = 0
        stream_seconds = 0.0

        for chunk in creative_model.stream(post_messages):
            if chunk.text:
                print(chunk.text, end="", flush=True)

            # Stream usage information is normally available on the final chunk.
            if chunk.usage_metadata:
                stream_tokens = chunk.usage_metadata.get("total_tokens", 0)

            stream_metadata = chunk.response_metadata

            if stream_metadata.get("total_duration"):
                stream_seconds = (
                    stream_metadata["total_duration"] / 1_000_000_000
                )
            elif (
                stream_metadata.get("prompt_eval_count") is not None
                and stream_metadata.get("eval_count") is not None
            ):
                stream_tokens = (
                    stream_metadata["prompt_eval_count"]
                    + stream_metadata["eval_count"]
                )

        print()

        posts += 1
        total_tokens += stream_tokens
        total_seconds += stream_seconds

    # Answer prices directly from the facts dictionary.
    elif command.startswith("/price"):
        parts = user_input.split(maxsplit=1)

        if len(parts) < 2:
            print("Studio: Please provide a product name.")
            continue

        item = parts[1].strip().lower()
        price = facts["prices"].get(item)

        # Why: Dictionary lookup avoids AI price hallucinations and saves tokens.
        if price is None:
            print(f"Studio: Sorry, {item.title()} is not on our menu.")

        elif price == 0:
            print(f"Studio: {item.title()} is coming soon.")

        else:
            print(f"Studio: {item.title()} costs {price:,} PKR.")

        price_answers += 1

    # Any other input is treated as a customer chat question.
    else:
        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # Why: Keep the system message and only the most recent conversation messages.
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = precise_model.invoke(messages)

        messages.append(
            {
                "role": "assistant",
                "content": response.text,
            }
        )

        print(f"Studio: {response.text}")

        chat_answers += 1

        total_tokens += response.usage_metadata.get("total_tokens", 0)
        total_seconds += (
            response.response_metadata.get("total_duration", 0)
            / 1_000_000_000
        )

        print(
            f"        (memory: {len(messages)} messages, "
            f"{response.usage_metadata.get('input_tokens', 0)} tokens sent)"
        )


# Final session report.
print("=" * 50)
print("Session report")
print(
    f"Chat answers: {chat_answers} | "
    f"Menu descriptions: {menu_descriptions} | "
    f"Posts: {posts} | "
    f"Price answers: {price_answers}"
)
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50)