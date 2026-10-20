
"""
Task 1.5: AI Model Profile Card

Displays an AI model's profile, data types, and estimated chat cost.
"""

model_name: str = "llama3.2"
context_window: int = 128000
price_per_1k_tokens: float = 0.5
runs_locally: bool = True

print("--- AI Model Profile Card ---")

print(f"Model: {model_name} {type(model_name)}")

print(f"Context window: {context_window} tokens {type(context_window)}")

print(f"Price per 1K tokens: {price_per_1k_tokens} PKR {type(price_per_1k_tokens)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# why: here we are asking the user tokens per chat so we can create estimate cost according to that token usage
tokens_per_chat: int = int(input("Tokens per chat: "))
print(f"Tokens per chat: {tokens_per_chat}")

# Why: rounding to two decimals is easy to read
estimated_cost: float = round(
    (tokens_per_chat / 1000) * price_per_1k_tokens, 2
)
print(f"Estimated cost: {estimated_cost} PKR")

# Stretch
chats_per_day: int = int(input("Chats per day: "))
monthly_cost: float = round(estimated_cost * chats_per_day * 30, 2)

print(f"Estimated monthly cost: {monthly_cost} PKR")