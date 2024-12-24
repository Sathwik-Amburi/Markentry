from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
from markentry.utils import make_supervisor_node

from markentry.nodes import (
	market_expert_node,
	company_expert_node,
	country_expert_node,
	competitor_expert_node,
	product_expert_node,
)

# Initialize the workflow with the appropriate state
workflow = StateGraph(MessagesState)

# Make a Supervisor Node
llm = ChatOpenAI(model='gpt-4o-mini')
market_research_supervisor_node = make_supervisor_node(
	llm,
	[
		'company_expert',
		'competitor_expert',
		'market_expert',
		'product_expert',
		'country_expert',
	],
)

# Add the 'supervisor' node
workflow.add_node('supervisor', market_research_supervisor_node)

# Add nodes
workflow.add_node('market_expert', market_expert_node)
workflow.add_node('company_expert', company_expert_node)
workflow.add_node('country_expert', country_expert_node)
workflow.add_node('competitor_expert', competitor_expert_node)
workflow.add_node('product_expert', product_expert_node)

# Connect 'START' to 'supervisor'
workflow.add_edge(START, 'supervisor')


# Connect 'market_expert' to all expert nodes
workflow.add_edge('market_expert', 'company_expert')
workflow.add_edge('market_expert', 'country_expert')
workflow.add_edge('market_expert', 'competitor_expert')
workflow.add_edge('market_expert', 'product_expert')


# Compile the workflow graph with the updated configuration
workflow_graph = workflow.compile()
