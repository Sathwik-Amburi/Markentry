from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from markentry.tools import tavily_search, make_handoff_tool

llm = ChatOpenAI(model='gpt-4o-mini')

system_message = """
You are the Market Research Agent for a company specified by the user. 
Your role is to analyze markets, evaluate opportunities, assess risks, and provide actionable recommendations for market entry or growth. 
You use structured business analysis frameworks like SWOT, PESTLE, and Porter’s Five Forces to ensure strategic, data-driven insights. 
Your responses should be clear, concise, and actionable, tailored to support the company’s decision-making.
"""
theoretical_market_expert_tools = [
    tavily_search,
    make_handoff_tool(agent_name="company_expert"),
    make_handoff_tool(agent_name="competitor_expert"),
    make_handoff_tool(agent_name="country_expert"),
    make_handoff_tool(agent_name="product_expert"),
]

market_expert = create_react_agent(
	llm, tools=theoretical_market_expert_tools, state_modifier=system_message
)
