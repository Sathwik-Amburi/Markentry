from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from typing import Dict, Any, Optional
from markentry.state import AgentState, PlannerState
import json


class OrchestratorAgent:
	def __init__(self, model_name='gpt-4o', temperature=0):
		self.llm = ChatOpenAI(model=model_name, temperature=temperature)
		self.original_task: Optional[
			str
		] = """You are an orchestrator responsible for coordinating multiple AI agents: Market Research Agent, Product Expert, Company Expert, Competitor Expert, and Country Expert. 
        Your primary role is to:
        1. Review the tasks and responses of individual agents.
        2. Assess the completeness of their outputs based on the overall objectives provided by the user.
        3. Identify gaps or missing aspects in the analysis.
        4. Propose actionable next steps to ensure all objectives are met.
        Your goal is to deliver a comprehensive and coordinated final output, ensuring all aspects of the analysis align with the user’s strategic goals."""

		self.prompt = ChatPromptTemplate.from_messages(
			[
				(
					'system',
					"""You are an orchestrator that coordinates interactions between multiple specialized agents.
                    Your tasks include:
                    - Reviewing the inputs and outputs of the Market Research Agent, Product Expert, Company Expert, Competitor Expert, and Country Expert.
                    - Determining whether the original user task has been fully addressed.
                    - Identifying missing aspects and proposing structured next steps to ensure all objectives are met.

                    Format your response as:
                    {
                        "complete": boolean,
                        "analysis": "Detailed assessment of progress and gaps",
                        "missing_aspects": ["list", "of", "missing", "items"],
                        "new_steps": ["step1", "step2"] # Only if incomplete
                    }
                    If all tasks are complete, confirm and summarize the findings in a comprehensive manner.""",
				),
				MessagesPlaceholder(variable_name='messages'),
			]
		)

	def store_user_task(self, task: str):
		self.original_task = task

	def evaluate_completion(self, final_answer: str) -> Dict[str, Any]:
		"""Evaluate if the final answer completely solves the original task"""
		messages = [
			SystemMessage(content='Evaluate if the solution meets all requirements.'),
			HumanMessage(
				content=f'Original Task:\n{self.original_task}\n\nFinal Answer:\n{final_answer}'
			),
		]
		chain = self.prompt | self.llm
		result = chain.invoke({'messages': messages})
		print(result)
		print(result.content)
		try:
			evaluation = json.loads(result.content)
			if not evaluation['complete']:
				# Reset planner state with new steps
				planner_state = PlannerState()
				planner_state.steps = evaluation['new_steps']
				return {
					'complete': False,
					'new_steps': evaluation['new_steps'],
					'analysis': evaluation['analysis'],
				}
			return {'complete': True, 'analysis': evaluation['analysis']}
		except Exception as e:
			print(f'Error parsing orchestrator response: {e}')
			return {'complete': False, 'error': str(e)}

	def is_complete(self, state: AgentState) -> bool:
		"""Check if we should continue the workflow"""
		messages = state['messages']
		if not messages:
			return True

		last_message = messages[-1]
		if (
			isinstance(last_message, AIMessage)
			and 'FINAL ANSWER' in last_message.content
		):
			evaluation = self.evaluate_completion(last_message.content)
			return not evaluation['complete']

		return True

	# def process_state(self, state: AgentState) -> Dict[str, Any]:
	#     messages = state.get('messages', [])

	#     # Create completion chain
	#     chain = self.prompt | self.llm

	#     # Process the current state
	#     result = chain.invoke({"messages": messages})

	#     return {
	#         "messages": result.content,
	#         "next_steps": self._extract_next_steps(result.content)
	#     }

	# def _extract_next_steps(self, content: str) -> List[Dict[str, Any]]:
	#     # Parse the content to extract structured next steps
	#     # This is a simplified version - expand based on your needs
	#     steps = []
	#     if "code_needed" in content.lower():
	#         steps.append({"type": "code", "action": "execute_python"})
	#     if "ask_user" in content.lower():
	#         steps.append({"type": "user_input", "action": "ask_user"})
	#     return steps
