from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from base_workflow.router import router
from base_workflow.nodes import agent_node, planner_node, benchmark_node
from base_workflow.state import AgentState
from base_workflow.tools import ask_user, tavily_search


workflow = StateGraph(AgentState)

workflow.add_node('planner', planner_node)
workflow.add_node('agent', agent_node)
workflow.add_node('benchmark', benchmark_node)
workflow.add_node(
	'call_tool',
	ToolNode([ask_user, tavily_search]),
)
workflow.add_edge('planner', 'agent')
workflow.add_edge('call_tool', 'agent')
workflow.add_edge('agent', 'benchmark')
workflow.add_conditional_edges(
	'benchmark',
	router,
	{'continue': 'agent', 'call_tool': 'call_tool', 'end': END},
)
workflow.set_entry_point('planner')
