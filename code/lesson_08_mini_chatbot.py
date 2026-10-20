
"""
Task 1.8: Business Helper Bot

A simple clinic chatbot that answers common questions,
handles complaints, and tracks unanswered messages.
"""

print(
    "City Care Bot: Hi! Ask about timings, fees, location "
    "or appointments. Type 'bye' to exit."
)

user_name = input("City Care Bot: What is your name? ").strip().title()

message_count = 0
unanswered_count = 0
complaint_count = 0

while True:
    user_message = input(f"{user_name}: ").strip().lower()
    message_count += 1

    # Why: Checking for exit first prevents the bot from answering after goodbye.
    if user_message == "bye":
        print(f"City Care Bot: Take care, {user_name}!")
        break

    # Why: Complaints need priority because they may require human attention.
    if any(word in user_message for word in ["complaint", "late", "problem", "issue"]):
        complaint_count += 1
        print(
            "City Care Bot: Sorry about that. "
            "The clinic manager will call you today."
        )

    elif "agent" in user_message or "human" in user_message:
        print("City Care Bot: Connecting you to a human...")
        break

    # Why: checking for short greetings
    elif user_message in ["hi", "hello", "hey"]:
        print("City Care Bot: Hello! How can I help you today?")

    elif any(word in user_message for word in ["timings", "hours", "open", "close"]):
        print(
            "City Care Bot: We are open 10 am to 8 pm, "
            "Monday to Saturday."
        )

    elif any(word in user_message for word in ["fee", "fees", "price", "cost"]):
        print("City Care Bot: Consultation fee is 2,000 PKR.")

    elif any(word in user_message for word in ["location", "address", "where"]):
        print(
            "City Care Bot: We are located in Lahore. "
            "Please contact us for the exact address."
        )

    elif any(word in user_message for word in ["appointment", "book", "booking"]):
        print("City Care Bot: Please call the clinic to book an appointment.")

    else:
        unanswered_count += 1

        ai_prompt = (
            "You are the friendly assistant of City Care Clinic. "
            f"Answer in 2 lines: {user_message[:150]}"
        )

        print(
            "City Care Bot: I am not sure yet."
        )

print("========================================")
print(
    f"Chat summary: {message_count} messages, "
    f"{unanswered_count} unanswered, "
    f"{complaint_count} complaints."
)