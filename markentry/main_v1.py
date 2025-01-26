from langchain_core.runnables import RunnableConfig
from markentry.workflow import graph
from langgraph.types import Command
from markentry.tools.ai_message_to_report import generate_report_from_markdown
from langchain_openai import ChatOpenAI

import uuid
import os


def main():
	# List of user inputs, preserving your example sequence
	inputs = [
		# 1st round of conversation
		{
			'messages': [
				{
					'role': 'user',
					'content': 'i want to explore entering the autonomous military drone market in the USA. What are some key considerations?',
				}
			]
		},
		# 2nd round of conversation: using Command resume
		Command(
			resume='Could you recommend an ideal segment or target audience to focus on for the initial entry?'
		),
		# 3rd round of conversation: using Command resume
		Command(
			resume='Could you suggest complementary industries or partnerships to enhance our entry strategy?'
		),
	]

	# Configuration
	thread_config: RunnableConfig = {
		'configurable': {'thread_id': uuid.uuid4()},
		'recursion_limit': 150,
	}

	# Keep track of all user and AI messages
	ai_respond_results = []

	# Run the conversation turns
	for idx, user_input in enumerate(inputs):
		print()
		print(f'--- Conversation Turn {idx + 1} ---')
		print()

		# Print user input to terminal
		if isinstance(user_input, dict) and 'messages' in user_input:
			# It's a new query
			user_msg = user_input['messages'][0]['content']
		else:
			# It's a resume command
			user_msg = user_input.resume

		print(f'User: {user_msg}\n')
		ai_respond_results.append(f'User: {user_msg}')

		# Stream the graph responses
		for update in graph.stream(
			user_input,
			config=thread_config,
			stream_mode='updates',
		):
			for node_id, value in update.items():
				if isinstance(value, dict) and value.get('messages', []):
					last_message = value['messages'][-1]
					if isinstance(last_message, dict) or last_message.type != 'ai':
						continue
					# Print AI message to terminal
					print(f'{node_id}: {last_message.content}')
					ai_respond_results.append(f'{node_id}: {last_message.content}')

	# --------------------------------
	# AFTER the conversation is done,
	# save the conversation log and generate a PDF
	# --------------------------------

	output_dir = 'markentry/outputs'
	os.makedirs(output_dir, exist_ok=True)

	# File path for the conversation log
	output_file_path = os.path.join(output_dir, 'conversation_log.md')

	# If an old log file exists, remove it
	if os.path.exists(output_file_path):
		os.remove(output_file_path)
		print(f"Existing file 'conversation_log.md' deleted from {output_dir}")

	# Save conversation log as Markdown
	with open(output_file_path, 'w', encoding='utf-8') as md_file:
		md_file.write('# Conversation Log\n\n')
		for entry in ai_respond_results:
			md_file.write(f'{entry}\n\n')
	print(f"Conversation log saved as 'conversation_log.md' at {output_file_path}")

	# Use your model to generate a more polished report from the Markdown
	model = ChatOpenAI(model='gpt-4o-mini')
	md_file_path = output_file_path

	# Generate the report (optionally PDF) and rewrite
	output_pdf_path = os.path.join(output_dir, 'rewrite_conversation_log.pdf')
	report_content = generate_report_from_markdown(md_file_path, model, output_dir)

	# Save the "rewritten" content to another Markdown file
	rewrite_output_md_path = os.path.join(output_dir, 'rewrite_conversation_log.md')

	if isinstance(report_content, (list, dict)):
		report_content_str = (
			'\n'.join([str(item) for item in report_content])
			if isinstance(report_content, list)
			else str(report_content)
		)
	else:
		report_content_str = str(report_content)

	with open(rewrite_output_md_path, 'w', encoding='utf-8') as md_file:
		md_file.write(report_content_str)

	print(f'Report saved to Markdown file at: {rewrite_output_md_path}')


if __name__ == '__main__':
	main()
