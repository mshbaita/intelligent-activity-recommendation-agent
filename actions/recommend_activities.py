from copy import deepcopy

from actions.base import BaseAction, ActionType
from llm_engine import OpenAIChatLLM
from state import State


class RecommendActivitiesAction(BaseAction):

    name = "RECOMMEND_ACTIVITIES"
    type = ActionType.AGENT_RESPONSE
    PROMPT_TEMPLATE = """You are customized tourist guide you have to give people suggestion of certain activities that can be done in specific location, weather condition (Summer or Winter) based on start and end date, and other important information provided below, generate a list of activities as an output BASED ON BELOW INFO.

            IMPORTANT INFORMATION
            1- Number of Adults= {num_adults} 
            2- Age of the adults = {ages_of_adults}
            3- Gender of adults = {gender_of_adults}
            4- Number of children = {num_children}
            5- Age of the children = {ages_of_children}
            6- Gender of children = {gender_of_children}
            7- Location = {location}
            8- Interests = {interests}
            9- Start date = {start_date}.
            10- End date = {end_date}
            
            INFORMATION ABOUT THE TARGET LOCATION USING GOOGLE SEARCH
            {search_result}

            output:
            """.strip()

    def __init__(self):
        self._chat_llm = OpenAIChatLLM()

    def execute(self, state: State):
        prompt = self.PROMPT_TEMPLATE.format(
            search_result=state.search_result,
            **state.required_slots,
            **state.optional_slots
        )
        messages = deepcopy(state.message_history)
        messages.append({"role": "system", "content": prompt})
        return self._chat_llm(messages=messages)

