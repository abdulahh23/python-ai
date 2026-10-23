
"""
Module 1 Checkpoint 2: AI Front Desk

A front desk assistant for Sweet Crumbs Bakery that answers FAQs,
calculates order prices, routes unanswered questions to suitable
AI models, and prepares a session report for the owner.
"""

# Constants: keep business settings in UPPER_CASE.
BOT_NAME = "Sweet Crumbs Desk"
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000
CLOUD_PRICE_PER_1K_TOKENS = 0.1
BULK_DISCOUNT_RATE = 0.10

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

customer_name = input(f"{BOT_NAME}: What is your name? ").strip().title()

message_count = 0
answered_by_rules = 0
unanswered_count = 0
quote_count = 0
total_quoted_value = 0.0
total_ai_cost = 0.0
complaint_count = 0

while True:
    user_message = input(f"{customer_name}: ").strip().lower()

    # Why: Empty messages should not waste a reply or affect the report.
    if user_message == "":
        print(f"{BOT_NAME}: Please enter a message.")
        continue

    message_count += 1

    # Why: Complaints must be handled before general rules or AI fallback.
    if (
    "refund" in user_message
    or "complaint" in user_message
    or " late " in f" {user_message} "
    ):
        complaint_count += 1
        answered_by_rules += 1
        print(
            f"{BOT_NAME}: Sorry about that. "
            "A manager will call you within 1 hour."
        )

    elif "agent" in user_message or "human" in user_message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break

    elif user_message == "bye":
        print(f"{BOT_NAME}: Goodbye, {customer_name}!")
        break

    elif user_message == "/quote":
        item_name = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # Why: Checking digits first prevents letters from crashing int().
        if not quantity_text.isdigit():
            print(f"{BOT_NAME}: Please enter the quantity using digits.")
        elif int(quantity_text) <= 0:
            print(f"{BOT_NAME}: Quantity must be greater than zero.")
        else:
            quantity = int(quantity_text)

            if item_name == "cupcake":
                item_price = 250
            elif item_name == "brownie":
                item_price = 300
            elif item_name == "chocolate cake":
                item_price = 1500
            else:
                item_price = 0

            if item_price == 0:
                print(
                    f"{BOT_NAME}: Sorry, {item_name} "
                    "is not on our menu."
                )
            else:
                subtotal = item_price * quantity

                # Why: Bulk discounts reward customers placing large orders.
                if quantity >= 10:
                    discount = subtotal * BULK_DISCOUNT_RATE
                else:
                    discount = 0

                discounted_subtotal = subtotal - discount

                # Why: Delivery is free only when the discounted subtotal
                # reaches the specified limit.
                if discounted_subtotal >= FREE_DELIVERY_LIMIT:
                    delivery_cost = 0
                else:
                    delivery_cost = DELIVERY_FEE

                total_cost = discounted_subtotal + delivery_cost

                quote_count += 1
                answered_by_rules += 1
                total_quoted_value += total_cost

                print(
                    f"{BOT_NAME}: {quantity} x {item_name} = "
                    f"{subtotal:,.0f} PKR"
                )
                print(
                    f"     Discount: -{discount:,.0f} PKR | "
                    f"Delivery: {delivery_cost:,.0f} PKR"
                )
                print(f"     Total: {total_cost:,.0f} PKR")

    # FAQ rules
    elif (
        "hi" == user_message
        or user_message.startswith("hi ")
        or user_message == "hello"
        or user_message.startswith("hello ")
        or user_message == "hey"
        or user_message.startswith("hey ")
    ):
        answered_by_rules += 1
        print(f"{BOT_NAME}: Hello! How can I help you today?")

    elif (
        "hours" in user_message
        or "timings" in user_message
        or "opening time" in user_message
        or "open" in user_message
        or "close" in user_message
    ):
        answered_by_rules += 1
        print(f"{BOT_NAME}: We are open 9 am to 10 pm, every day.")

    elif "location" in user_message or "where" in user_message:
        answered_by_rules += 1
        print(
            f"{BOT_NAME}: We are located in Lahore. "
            "Please contact us for the exact address."
        )

    elif (
        "delivery" in user_message
        or "deliver" in user_message
        or "shipping" in user_message
    ):
        answered_by_rules += 1
        print(
            f"{BOT_NAME}: Delivery costs {DELIVERY_FEE} PKR. "
            f"It is free for orders of {FREE_DELIVERY_LIMIT} PKR "
            "or more after discount."
        )

    elif (
        "fee" in user_message
        or "fees" in user_message
        or "price" in user_message
        or "prices" in user_message
        or "menu" in user_message
    ):
        answered_by_rules += 1
        print(
            f"{BOT_NAME}: Cupcakes are 250 PKR each, brownies are "
            "300 PKR each, and chocolate cakes are 1,500 PKR each. "
            "Type /quote for an order estimate."
        )

    # AI fallback for questions that rules cannot answer
    else:
        unanswered_count += 1

        cleaned_question = user_message.capitalize()[:150]
        estimated_tokens = round(len(cleaned_question) / 4)

        # Why: Private questions should use a local model instead of
        # sending personal details to a cloud service.
        if (
            "phone" in user_message
            or "cnic" in user_message
            or "address" in user_message
        ):
            chosen_model = "llama3.2 (local, private)"
            estimated_cost = 0.0
        else:
            chosen_model = "small cloud model (cheap)"
            estimated_cost = (
                estimated_tokens / 1000
            ) * CLOUD_PRICE_PER_1K_TOKENS

        total_ai_cost += estimated_cost

        ai_prompt = f"""You are the assistant of Sweet Crumbs bakery.
Answer {customer_name} in 2 short lines. Question: {cleaned_question}"""

        print(
            f"{BOT_NAME}: Good question! Routed to: {chosen_model} "
            f"(~{estimated_tokens} tokens)"
        )
        print(f"     Prompt: {ai_prompt}")
        print(f"     Estimated cost: {estimated_cost:.4f} PKR")

print("=" * 50)
print("Session report")
print(
    f"Messages: {message_count} | Answered by rules: "
    f"{answered_by_rules} | Unanswered: {unanswered_count}"
)
print(
    f"Quotes: {quote_count} | Quoted value: "
    f"{total_quoted_value:,.0f} PKR"
)
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print(f"Complaints received: {complaint_count}")
print("=" * 50)