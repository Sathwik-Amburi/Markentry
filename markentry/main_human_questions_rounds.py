from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from markentry.workflow import graph
from langgraph.types import Command, interrupt
from markentry.tools.ai_message_to_report import generate_report_from_markdown
from langchain_openai import ChatOpenAI
import uuid
import os


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

# saving all ai responses for PDF export
ai_respond_results = []

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

    # Log user input
    ai_respond_results.append(f"User: {user_input}")

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
                    ai_respond_results.append(f"{node_id}: {last_message.content}")
                else:
                    print("false content")

    print("\n")
    conversation_turn += 1

# Directory where the output PDF will be saved
output_dir = "/Users/taizhang/Desktop/Markentry/markentry/outputs"

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)
# File path for the conversation log
output_file_path = os.path.join(output_dir, "conversation_log.md")

# Check if the file exists
if os.path.exists(output_file_path):
    # If the file exists, delete it
    os.remove(output_file_path)
    print(f"Existing file 'conversation_log.md' deleted from {output_dir}")

with open(output_file_path, "w", encoding="utf-8") as md_file:
    md_file.write("# Conversation Log\n\n")
    for entry in ai_respond_results:
        md_file.write(f"{entry}\n\n")        
print(f"Conversation log saved as 'conversation_log.md' at {output_file_path}")

# regenerate the 'conversation_log.md' into 'report_content'
model = ChatOpenAI(model="gpt-4o-mini")
# Load the ai_response content
md_file_path = output_file_path
# Directory where the output .md file will be saved
output_dir = "/Users/taizhang/Desktop/Markentry/markentry/outputs"
output_pdf_path = os.path.join(output_dir, "rewrite_conversation_log.pdf")
# Generate the report and save as Markdown
report_content = generate_report_from_markdown(md_file_path, model, output_dir)


###save the report_content into 'rewrite_conversation_log.md'
# Directory where the output .md file will be saved
rewrite_output_dir = "/Users/taizhang/Desktop/Markentry/markentry/outputs"
rewrite_output_md_path = os.path.join(output_dir, "rewrite_conversation_log.md")

# Ensure the directory exists
os.makedirs(rewrite_output_dir, exist_ok=True)

# Ensure `report_content` is a string
if isinstance(report_content, (list, dict)):
    # Convert list or dict to string
    report_content_str = "\n".join([str(item) for item in report_content]) if isinstance(report_content, list) else str(report_content)
else:
    report_content_str = str(report_content)

# Save the report content to a .md file
with open(rewrite_output_md_path, "w", encoding="utf-8") as md_file:
    md_file.write(report_content_str)

print(f"Report saved to Markdown file at: {rewrite_output_md_path}")

###################################################################################################################
#  question examples:
#  i want to explore entering the autonomous military drone market in the USA. What are some key considerations?
#  resume：Could you recommend an ideal segment or target audience to focus on for the initial entry?
#  resume：Could you suggest complementary industies or partnerships to enhance our entry strategy?