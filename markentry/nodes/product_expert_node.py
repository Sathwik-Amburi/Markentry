# Helper function to create a node for a given agent
from markentry.agents import product_expert
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from typing import Literal


def product_expert_node(state: MessagesState) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "theoretical_market_expert", "human"]]:
	response = product_expert.invoke(state)
	return Command(update=response, goto='human')

