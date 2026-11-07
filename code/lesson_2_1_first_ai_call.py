
"""Task 2.1: Ask an AI tutor to explain a topic at the student's level."""

from langchain.chat_models import init_chat_model


topic = input("Topic: ").strip()
level = input("Level (beginner or expert): ").strip()

# Why: The system message controls the AI's role and keeps answers at the requested level.
system_message = (
    f"You are a helpful Python tutor. Explain the topic at a {level} level. "
    "For beginners, use simple language and examples. "
    "For experts, include technical details. "
    "Keep your answer concise, around 3 to 5 sentences."
)

llm = init_chat_model("ollama:gemma3:1b", temperature=0.2)

response = llm.invoke(
    [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Explain: {topic}"},
    ]
)

print("=" * 40)
print(response.text)
print("=" * 40)

# Why: Token usage helps estimate how much of the model's context was used.
total_tokens = response.usage_metadata["total_tokens"]

# Why: Ollama reports duration in nanoseconds, so convert it to seconds.
total_seconds = response.response_metadata["total_duration"] / 1_000_000_000

print(f"{total_tokens} tokens in {total_seconds:.1f} seconds")