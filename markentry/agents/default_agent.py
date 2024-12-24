from langchain_openai import ChatOpenAI

from markentry.tools import (
	ask_user,
	execute_python,
	get_available_cities,
	get_restaurants_and_menu_in_city,
	order_pizza,
)
from markentry.utils import create_agent

llm = ChatOpenAI(model='gpt-4o-mini')

default_agent = create_agent(
	llm,
	[
		ask_user,
		execute_python,
		get_available_cities,
		get_restaurants_and_menu_in_city,
		order_pizza,
	],
	'Dont invent anything.',
)
