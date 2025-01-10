# Helper function to create a node for a given agent
from markentry.agents import market_expert
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from typing import Literal


def market_expert_node(state: MessagesState) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "product_expert", "human"]]:
	response = market_expert.invoke(state)
	return Command(update=response, goto='human')
