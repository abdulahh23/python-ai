
"""Task 2.4: Generate product descriptions for the bakery menu in one batch."""

from langchain.chat_models import init_chat_model


products = {
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Cookies": 150,
    "Old Stock": 0,
}

# Why: Creating the model once avoids repeatedly initializing it inside the loop.
llm = init_chat_model("ollama:gemma3:1b", temperature=0.2)

results = []

# Why: Starting accumulators at zero allows us to calculate the total usage.
total_tokens = 0
total_seconds = 0.0

for name, price in products.items():

    # Why: Items without a price should not generate an AI request.
    if price == 0:
        print(f"Skipping {name.lower()} (no price)")
        continue

    prompt = (
        f"Write a single attractive sentence describing {name} "
        f"for Sweet Crumbs Bakery in Lahore. "
        f"Its price is {price} PKR. "
        "Keep the description short and suitable for a bakery menu."
    )

    response = llm.invoke(prompt)

    description = response.text
    tokens = response.usage_metadata["total_tokens"]

    # Ollama reports total_duration in nanoseconds.
    seconds = response.response_metadata["total_duration"] / 1_000_000_000

    total_tokens += tokens
    total_seconds += seconds

    results.append(
        {
            "item": name,
            "price": price,
            "text": description,
        }
    )

print("=" * 50)

for number, product in enumerate(results, start=1):
    print(f"{number}. {product['item']} ({product['price']} PKR)")
    print(f"   {product['text']}")

print("=" * 50)

print(
    f"{len(results)} descriptions, "
    f"{total_tokens} tokens, "
    f"{total_seconds:.1f} seconds"
)