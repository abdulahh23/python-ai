
"""Generate three ready-to-use AI prompts for local business owners."""

# Collecting the business name helps personalise all three prompts.
business_name = input("Business name: ")

business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# Converting the budget to an integer allows it to be used as a numeric amount.
monthly_budget = int(input("Monthly budget (PKR): "))

print("\n=========================================")
print(f"       AI Prompt Kit for {business_name}")
print("=========================================")

# Naming the platform, audience and tone makes the marketing prompt more specific.
marketing_prompt = (
    f"Write a short Instagram post for {business_name}, a {business_type} in {city}.\n"
    f"Target {customers}. Friendly tone, 1 call to action."
)

print("\n[1] Marketing")
print(marketing_prompt)

# Giving the AI a role and a clear situation helps it produce an appropriate reply.
customer_service_prompt = (
    f"You are the manager of {business_name}. Write a polite reply to a customer\n"
    f"whose order arrived late. Apologise and offer a small discount."
)

print("\n[2] Customer Service")
print(customer_service_prompt)

# Including the actual budget helps keep the suggested ideas financially relevant.
growth_prompt = (
    f"Suggest 3 low-cost AI tools a {business_type} in {city} can use\n"
    f"to attract {customers} with a budget of {monthly_budget} PKR per month."
)

print("\n[3] Growth")
print(growth_prompt)

print("\n=========================================")
print("Tip: A good prompt names a role, a task, the audience and a tone or number.")
print("Vague prompts get vague answers.")
print("=========================================")
