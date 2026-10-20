
"""
Task 1.6: Prompt Cleaner

Cleans user input, measures the question, and builds a safe-sized AI prompt.
"""

user_name = input("Your name: ")
messy_question = input("Your question: ")

cleaned_name = user_name.strip().title()
cleaned_question = messy_question.strip().capitalize()

# Why: cleaning input makes the prompts more readable.
# Stretch: replacing bad words
cleaned_question = cleaned_question.replace("stupid", "***")

character_count = len(cleaned_question)
estimated_tokens = round(character_count / 4)

print("=" * 40)
print(f"Cleaned question: {cleaned_question}")
print(f"Characters: {character_count}, about {estimated_tokens} tokens")

# Why: lower() makes the keyword check work regardless of capitalization.
mentions_python = "python" in cleaned_question.lower()
print(f"Mentions Python: {mentions_python}")

prompt = f"""You are a friendly Python tutor.
Greet {cleaned_name} by name and answer in 3 short lines.
Question: {cleaned_question[:150]}"""

print("=" * 40)
print(prompt)

# Stretch: Estimating cost
price_per_1k_tokens = 0.5
estimated_cost = (estimated_tokens / 1000) * price_per_1k_tokens

print(f"Estimated cost: {estimated_cost:.2f} PKR")