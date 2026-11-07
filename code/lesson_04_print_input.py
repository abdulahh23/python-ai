"""Collect business details and generate an AI prompt."""

#why: Asking for the name makes the greeting more personal.
name = input("Your name: ")

business = input("Business type: ")
problem = input("Biggest problem: ")

print(f"\nWelcome, {name}!")
print("--- Your AI Prompt ---")

#why: Focusing on one business problem helps generate relevant solutions.
prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."

print(prompt)