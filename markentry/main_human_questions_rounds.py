from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from markentry.workflow import graph
from langgraph.types import Command, interrupt
import uuid

# Configuration
thread_config: RunnableConfig = {
    'configurable': {"thread_id": uuid.uuid4()},
    'recursion_limit': 150
}

def is_command(input_str: str) -> bool:
    """
    Check if the input is a follow-up (resume) command or a new question.
    """
    return input_str.lower().startswith("resume:")

# Main conversation loop
print("Welcome to the Autonomous Drone Market Explorer!")
print("Type your questions or follow-up-questions (e.g., 'resume: ...'). Type 'exit' to quit.\n")

conversation_turn = 1
user_input = None

while True:
    print(f"--- Conversation Turn {conversation_turn} ---")
    user_input = input("User: ").strip()
    
    if user_input.lower() == "exit":
        print("Exiting the conversation. Goodbye!")
        break

    # Prepare input based on whether it’s a Command or a new query
    if is_command(user_input):
        graph_input = Command(resume=user_input[len("resume:"):].strip())
        print("Follow up question recognized!")
    else:
        graph_input = {"messages": [{"role": "user", "content": user_input}]}

    print("\nProcessing...\n")

    # Process the graph input and stream responses
    for update in graph.stream(
        graph_input,
        config=thread_config,
        stream_mode="updates",
    ):
        for node_id, value in update.items():
            if isinstance(value, dict) and value.get("messages", []):
                last_message = value["messages"][-1]
                if isinstance(last_message, dict):
                    continue
                elif last_message.type == "ai":
                    print(f"{node_id}: {last_message.content}")
                else:
                    print("false content")

    print("\n")
    conversation_turn += 1


###################################################################################################################
#  question examples:
#  i want to explore entering the autonomous military drone market in the USA. What are some key considerations?
#  resume：Could you recommend an ideal segment or target audience to focus on for the initial entry?
#  resume：Could you suggest complementary industies or partnerships to enhance our entry strategy?