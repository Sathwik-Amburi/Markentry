# Helper function to create a node for a given agent
from markentry.agents import company_expert
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from typing import Literal


def company_expert_node(state: MessagesState) -> Command[Literal["competitor_expert", "country_expert", "product_expert", "theoretical_market_expert", "human"]]:
	response = company_expert.invoke(state)
	return Command(update=response, goto='human')
