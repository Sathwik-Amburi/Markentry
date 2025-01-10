from langchain_core.runnables import RunnableConfig
from markentry.workflow import graph
from langgraph.types import Command
import uuid


def main():
	inputs = [
		# 1st round of conversation,
		{
			'messages': [
				{
					'role': 'user',
					'content': 'i want to explore entering the autonomous military drone market in the USA. What are some key considerations?',
				}
			]
		},
		# Since we're using `interrupt`, we'll need to resume using the Command primitive.
		# 2nd round of conversation,
		Command(
			resume='Could you recommend an ideal segment or target audience to focus on for the initial entry?'
		),
		# 3rd round of conversation,
		Command(
			resume='Could you suggest complementary industries or partnerships to enhance our entry strategy?'
		),
	]

<<<<<<< HEAD
for idx, user_input in enumerate(inputs):
    print()
    print(f"--- Conversation Turn {idx + 1} ---")
    print()
    print(f"User: {user_input}")
    print()
    for update in graph.stream(
        user_input,
        config=thread_config,
        stream_mode="updates",
    ):
        for node_id, value in update.items():
            if isinstance(value, dict) and value.get("messages", []):
                last_message = value["messages"][-1]
                if isinstance(last_message, dict) or last_message.type != "ai":
                    continue
                print(f"{node_id}: {last_message.content}")
=======
	thread_config: RunnableConfig = {
		'configurable': {'thread_id': uuid.uuid4()},
		'recursion_limit': 150,
	}

	for idx, user_input in enumerate(inputs):
		print()
		print(f'--- Conversation Turn {idx + 1} ---')
		print()
		print(f'User: {user_input}')
		print()
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
					print(f'{node_id}: {last_message.content}')


if __name__ == '__main__':
	main()
>>>>>>> d28996abbab6940f4cf3f5935067d33af54f2be5
