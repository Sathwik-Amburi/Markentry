from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from markentry.state import AgentState
from markentry.tools.retriever_tool import retriever_tool
from markentry.utils import rag_utils
from langgraph.prebuilt import tools_condition

from markentry.nodes import (
	market_expert_node,
	company_expert_node,
	country_expert_node,
	competitor_expert_node,
	product_expert_node,
	human_node,
)

# Initialize the workflow with the appropriate state
builder = StateGraph(AgentState)

# Initialize the Language Model
llm = ChatOpenAI(model='gpt-4o-mini')
builder.add_node('company_expert', company_expert_node)

# RAG
# builder.add_node('agent', rag_utils.agent)  # agent
retrieve = ToolNode([retriever_tool])
builder.add_node('retrieve', retrieve)  # retrieval
builder.add_node('rewrite', rag_utils.rewrite)  # Re-writing the question

builder.add_node(
	'generate', rag_utils.generate
)  # Generating a response after we know the documents are relevant

# Decide whether to retrieve
builder.add_conditional_edges(
	'company_expert',
	# Assess agent decision
	tools_condition,
	{
		# Translate the condition outputs to nodes in our graph
		'tools': 'retrieve',
	},
)

# Edges taken after the `action` node is called.
builder.add_conditional_edges(
	'retrieve',
	# Assess agent decision
	rag_utils.grade_documents,
)
builder.add_edge('rewrite', 'company_expert')


builder.add_node('competitor_expert', competitor_expert_node)
builder.add_node('country_expert', country_expert_node)
builder.add_node('product_expert', product_expert_node)
builder.add_node('theoretical_market_expert', market_expert_node)
# This adds a node to collect human input, which will route
# back to the active agent.
builder.add_node('human', human_node)

# We'll always start with a general travel advisor.
builder.add_edge(START, 'theoretical_market_expert')
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
