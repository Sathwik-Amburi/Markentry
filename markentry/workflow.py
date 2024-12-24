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

# Initialize the Language Model
llm = ChatOpenAI(model='gpt-4o-mini')

# Make a Supervisor Node
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

# Define all expert nodes in a dictionary for easy management
expert_nodes = {
	'market_expert': market_expert_node,
	'company_expert': company_expert_node,
	'country_expert': country_expert_node,
	'competitor_expert': competitor_expert_node,
	'product_expert': product_expert_node,
}

# Add all expert nodes to the workflow
for node_name, node in expert_nodes.items():
	workflow.add_node(node_name, node)

# Connect 'START' to 'supervisor'
workflow.add_edge(START, 'supervisor')

# List of all nodes to be interconnected (excluding 'START')
all_nodes = ['supervisor'] + list(expert_nodes.keys())

# Add edges between every pair of nodes (excluding self-connections)
for source_node in all_nodes:
	for target_node in all_nodes:
		if source_node != target_node:
			workflow.add_edge(source_node, target_node)

# Compile the workflow graph with the updated configuration
workflow_graph = workflow.compile()
