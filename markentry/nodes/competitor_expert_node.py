from langchain.schema import AIMessage
from markentry.agents.competitor_expert import competitor_expert
from markentry.state import AgentState
from markentry.agents.planner_agent import planner_state


def competitor_expert_node(state: AgentState) -> AgentState:
	if planner_state.steps and planner_state.current_step < len(planner_state.steps):
		# Execute current step
		result = competitor_expert.invoke({'messages': state['messages']})
		if not isinstance(result, AIMessage):
			raise ValueError('Agent did not return AIMessage')

		# Increment step counter after execution
		planner_state.increment_step()
		return {'messages': [result]}

	# Normal execution without steps
	result = competitor_expert.invoke({'messages': state['messages']})
	if not isinstance(result, AIMessage):
		raise ValueError('Agent did not return AIMessage')
	return {'messages': [result]}
