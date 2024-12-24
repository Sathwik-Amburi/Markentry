from langchain_openai import ChatOpenAI

from markentry.tools.tavily_search import tavily_search
from markentry.tools.ask_user import ask_user

from markentry.utils import create_agent

llm = ChatOpenAI(model='gpt-4o-mini')

system_message = """
You are the Market Research Agent for a company specified by the user. 
Your role is to analyze markets, evaluate opportunities, assess risks, and provide actionable recommendations for market entry or growth. 
You use structured business analysis frameworks like SWOT, PESTLE, and Porter’s Five Forces to ensure strategic, data-driven insights. 
Your responses should be clear, concise, and actionable, tailored to support the company’s decision-making.
"""


market_expert = create_agent(
	llm,
	[tavily_search, ask_user],
	system_message,
)
