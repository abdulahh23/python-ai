
"""
Task 1.7: Smart Model Router

Routes AI requests to different models based on task type
and estimates the cost of each request.
"""

task_type = input("Task (code / private / chat): ").strip().lower()

estimated_tokens = int(input("Estimated tokens: "))

# Why: Private data should stay local for privacy.
if task_type == "private":
    model_name = "llama3.2 (local, Ollama)"
    price = 0.0

# Why: claude for better coding
elif task_type == "code":
    model_name = "claude (cloud, strong at code)"
    price = 0.8

else:
    model_name = "cheap chat model"
    price = 0.2

if estimated_tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

# Stretch: Check whether the user is paid.
is_paid_user = input("Is this a paid user? (yes/no): ").strip().lower()

if is_paid_user == "no" and estimated_tokens > 2000:
    print("Upgrade to send long requests.")

estimated_cost = (estimated_tokens / 1000) * price

print(f"Chosen model: {model_name}")
print(f"Estimated cost: {estimated_cost:.2f} PKR")