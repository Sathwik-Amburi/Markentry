from langchain_core.messages import HumanMessage
from langgraph.types import Command, interrupt
from langgraph.graph import MessagesState
from typing import Literal


# later imply real human UI interface.
def human_node(
    state: MessagesState, config
) -> Command[Literal["company_expert", "competitor_expert", "country_expert", "product_expert", "theoretical_market_expert", "human"]]:
    """A node for collecting user input."""

    user_input = interrupt(value="Ready for user input.")

    # identify the last active agent
    # (the last active node before returning to human)
    langgraph_triggers = config["metadata"]["langgraph_triggers"]
    if len(langgraph_triggers) != 1:
        raise AssertionError("Expected exactly 1 trigger in human node")

    active_agent = langgraph_triggers[0].split(":")[1]

    return Command(
        update={
            "messages": [
                {
                    "role": "human",
                    "content": user_input,
                }
            ]
        },
        goto=active_agent,
    )