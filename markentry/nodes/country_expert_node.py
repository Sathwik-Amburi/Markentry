# Helper function to create a node for a given agent
from markentry.agents import country_expert
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from typing import Literal


def country_expert_node(state: MessagesState) -> Command[Literal['supervisor']]:
	result = country_expert.invoke(state)
	return Command(
		update={
			'messages': [
				HumanMessage(content=result['messages'][-1].content, name='search')
			]
		},
		# We want our workers to ALWAYS "report back" to the supervisor when done
		goto='supervisor',
	)