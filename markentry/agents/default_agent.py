from langchain_openai import ChatOpenAI

from markentry.tools import (
	ask_user,
)
from markentry.utils import create_agent

llm = ChatOpenAI(model='gpt-4o-mini')

default_agent = create_agent(
	llm,
	[
		ask_user,
	],
	'Dont invent anything.',
)
