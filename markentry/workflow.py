from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from markentry.router import router
from markentry.nodes.planner_node import planner_node
from markentry.nodes.market_expert_node import market_expert_node
from markentry.nodes.country_expert_node import country_expert_node
from markentry.nodes.company_expert_node import company_expert_node
from markentry.nodes.competitor_expert_node import competitor_expert_node
from markentry.nodes.product_expert_node import product_expert_node

from markentry.state import AgentState
from markentry.tools.ask_user import ask_user
from markentry.tools.tavily_search import tavily_search

# Initialize the workflow with the agent state
workflow = StateGraph(AgentState)

# Add primary node
workflow.add_node('planner', planner_node)

# Add expert nodes
workflow.add_node('market_expert', market_expert_node)
workflow.add_node('country_expert', country_expert_node)
workflow.add_node('company_expert', company_expert_node)
workflow.add_node('competitor_expert', competitor_expert_node)
workflow.add_node('product_expert', product_expert_node)

# Add tool node
workflow.add_node(
	'call_tool',
	ToolNode([ask_user, tavily_search]),
)

# Define edges between planner and tools
workflow.add_edge('planner', 'call_tool')

# Connect planner directly to experts
workflow.add_edge('planner', 'market_expert')
workflow.add_edge('planner', 'country_expert')
workflow.add_edge('planner', 'company_expert')
workflow.add_edge('planner', 'competitor_expert')
workflow.add_edge('planner', 'product_expert')

# Connect experts back to planner
workflow.add_edge('market_expert', 'planner')
workflow.add_edge('country_expert', 'planner')
workflow.add_edge('company_expert', 'planner')
workflow.add_edge('competitor_expert', 'planner')
workflow.add_edge('product_expert', 'planner')

# Define edges from experts to tools
workflow.add_edge('market_expert', 'call_tool')
workflow.add_edge('country_expert', 'call_tool')
workflow.add_edge('company_expert', 'call_tool')
workflow.add_edge('competitor_expert', 'call_tool')
workflow.add_edge('product_expert', 'call_tool')

# Define conditional edges based on router outcomes for each expert
workflow.add_conditional_edges(
	'market_expert',
	router,
	{'continue': 'market_expert', 'call_tool': 'call_tool', 'end': END},
)
workflow.add_conditional_edges(
	'country_expert',
	router,
	{'continue': 'country_expert', 'call_tool': 'call_tool', 'end': END},
)
workflow.add_conditional_edges(
	'company_expert',
	router,
	{'continue': 'company_expert', 'call_tool': 'call_tool', 'end': END},
)
workflow.add_conditional_edges(
	'competitor_expert',
	router,
	{'continue': 'competitor_expert', 'call_tool': 'call_tool', 'end': END},
)
workflow.add_conditional_edges(
	'product_expert',
	router,
	{'continue': 'product_expert', 'call_tool': 'call_tool', 'end': END},
)

# Set the entry point of the workflow
workflow.set_entry_point('planner')

# Initialize memory saver
memory = MemorySaver()

# Compile the workflow graph with the memory saver
workflow_graph = workflow.compile(checkpointer=memory)
