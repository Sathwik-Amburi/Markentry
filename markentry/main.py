from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from markentry.workflow import workflow_graph

user_input = 'Give me market entry strategy for autonomous drones for aibus'

config: RunnableConfig = {'configurable': {'thread_id': '1'}, 'recursion_limit': 150}


def run_graph(input: Union[dict[str, Any], Any]):
	events = workflow_graph.stream(input, config, stream_mode='values')
	for event in events:
		if 'messages' in event:
			event['messages'][-1].pretty_print()
			print('----')


run_graph({'messages': [('user', user_input)]})
