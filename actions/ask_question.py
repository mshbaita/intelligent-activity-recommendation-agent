from copy import deepcopy

from actions.base import BaseAction, ActionType
from llm_engine import OpenAIChatLLM
from state import State


class AskQuestionAction(BaseAction):

    name = "ASK_QUESTION"
    type = ActionType.AGENT_RESPONSE
    PROMPT_TEMPLATE = """
You are a tourist guide agent assisting users with their inquiries. Given a conversation history between the user and the agent, your task is to generate a message to ask the user about missing information. The missing information will be provided in the prompt.

As a tourist guide agent, your next message should ask the user about the missing {missing_information}. Please provide the question without generating additional text.Consider None and not provided values as null values and you need to ask about
    """.strip()

    def __init__(self):
        self._chat_llm = OpenAIChatLLM()

    def execute(self, state: State):
        missing_info = ""
        for key, value in state.required_slots.items():
            # not provided or none is edge case can be solved with fine-tuning or few shot learning
            if not value:
                missing_info = key
                break
        if not missing_info:
            missing_info = "start date, end date"
        prompt = self.PROMPT_TEMPLATE.format(
            missing_information=missing_info
        )
        messages = deepcopy(state.message_history)
        # messages.insert(0, {"role": "system", "content": prompt})
        messages.append({"role": "system", "content": prompt})
        return self._chat_llm(messages=messages)
