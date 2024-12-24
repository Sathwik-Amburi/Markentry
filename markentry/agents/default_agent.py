from langchain_openai import ChatOpenAI

from markentry.utils import create_agent

llm = ChatOpenAI(model='gpt-4o-mini')

default_agent = create_agent(
	llm,
	[],
	'Dont invent anything.',
)
