from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from markentry.workflow import workflow_graph


def run_graph(input: Union[dict[str, Any], Any], config: RunnableConfig):
	"""Run the workflow graph with the given input and configuration."""
	events = workflow_graph.stream(input, config, stream_mode='values')
	for event in events:
		if 'messages' in event:
			event['messages'][-1].pretty_print()
			print('----')


def main():
	"""Main function to execute the market entry strategy workflow."""
	user_input = 'Give me market entry strategy for autonomous drones for Airbus'
	config: RunnableConfig = {
		'configurable': {'thread_id': '1'},
		'recursion_limit': 150,
	}

	run_graph({'messages': [('user', user_input)]}, config)


if __name__ == '__main__':
	main()
