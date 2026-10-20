role = input("AI role: ")
topic = input("Topic: ")
level = input("Level: ")

prompt = f"You are a {role}. Explain {topic} to a {level} in 3 bullet points."

print("Your Prompt:")
print(prompt)