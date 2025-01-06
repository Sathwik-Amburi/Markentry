from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
from markentry.utils import make_supervisor_node
from langgraph.checkpoint.memory import MemorySaver


from markentry.nodes import (
	market_expert_node,
	company_expert_node,
	country_expert_node,
	competitor_expert_node,
	product_expert_node,
    human_node
)

# Initialize the workflow with the appropriate state
builder = StateGraph(MessagesState)

# Initialize the Language Model
llm = ChatOpenAI(model='gpt-4o-mini')
builder.add_node("company_expert", company_expert_node)
builder.add_node("competitor_expert", competitor_expert_node)
builder.add_node("country_expert", country_expert_node)
builder.add_node("product_expert", product_expert_node)
builder.add_node("theoretical_market_expert", market_expert_node)
# This adds a node to collect human input, which will route
# back to the active agent.
builder.add_node("human", human_node)

# We'll always start with a general travel advisor.
builder.add_edge(START, "theoretical_market_expert")
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)