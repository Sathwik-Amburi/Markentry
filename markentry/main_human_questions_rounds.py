from langchain_core.runnables import RunnableConfig
from markentry.workflow import graph
from langgraph.types import Command
from markentry.tools.report_tool import generate_report, save_var_to_md, markdown_to_pdf
import uuid


# Configuration
thread_config: RunnableConfig = {
	'configurable': {'thread_id': uuid.uuid4()},
	'recursion_limit': 150,
}


def is_command(input_str: str) -> bool:
	"""
	Check if the input is a follow-up (resume) command or a new question.
	"""
	return input_str.lower().startswith('resume:')


# saving all ai responses for PDF export
ai_respond_results = []

# Main conversation loop
print('Welcome to the Autonomous Drone Market Explorer!')
print("Type your questions or follow-up-questions (e.g., 'resume: ...'). Type 'exit' to quit.\n")

conversation_turn = 1
user_input = None
predefined_inputs = [
	'What are the key capabilities and features of the product of Fortio Tactical?',
	'resume: What are the primary use cases for Fortion Tactical?',
	'resume: What are the advantages of using Fortion Tactical compared to alternatives?',
]

while True:
	print(f'--- Conversation Turn {conversation_turn} ---')
	if conversation_turn > len(predefined_inputs):
		user_input = input('User: ').strip()
		print('\nProcessing...\n')
	else:
		user_input = predefined_inputs[conversation_turn - 1]
		print(f'\nProcessing predefined question {conversation_turn} : {user_input}\n')

	if user_input.lower() == 'report':
		###Processing the report###
		conversation_turn += 1
		continue
	elif user_input.lower() == 'exit':
		print('Exiting the conversation. Goodbye!')
		break

	# Log user input
	ai_respond_results.append(f'User: {user_input}')

	# Prepare input based on whether it’s a Command or a new query
	if is_command(user_input):
		graph_input = Command(resume=user_input[len('resume:') :].strip())
		print('Follow up question recognized!')
	else:
		graph_input = {'messages': [{'role': 'user', 'content': user_input}]}

	# Process the graph input and stream responses
	for update in graph.stream(
		graph_input,
		config=thread_config,
		stream_mode='updates',
	):
		for node_id, value in update.items():
			if isinstance(value, dict) and value.get('messages', []):
				last_message = value['messages'][-1]
				if isinstance(last_message, dict):
					continue
				elif last_message.type == 'ai':
					print(f'{node_id}: {last_message.content}')
					ai_respond_results.append(f'{node_id}: {last_message.content}')
				else:
					print('false content')

	print('\n')
	conversation_turn += 1

# Directory where the output PDF will be saved
output_dir = 'outputs'

file_path = save_var_to_md(output_dir, ai_respond_results)
report_dir = generate_report(file_path)
markdown_to_pdf(report_dir)

###################################################################################################################
#  question examples:
#  i want to explore entering the autonomous military drone market in the USA. What are some key considerations?
#  resume：Could you recommend an ideal segment or target audience to focus on for the initial entry?
#  resume：Could you suggest complementary industies or partnerships to enhance our entry strategy?
