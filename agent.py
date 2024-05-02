from actions.ask_question import AskQuestionAction
from actions.base import ActionType
from actions.google_search import SearchActivitiesAction

from actions.recommend_activities import RecommendActivitiesAction
from actions.slot_extraction import SlotsExtractionAction
from llm_engine import OpenAILLM, OpenAIChatLLM

from state import State


class RecommendationAgent:

    def __init__(self):
        self._text_llm = OpenAILLM()
        self._chat_llm = OpenAIChatLLM()
        self._state = State()

    def _decision_making(self):
        actions = []
        if None in self._state.required_slots.values():
            actions.append(SlotsExtractionAction)
            actions.append(AskQuestionAction)
        else:
            actions.append(SlotsExtractionAction)
            #TODO: SERP API KEY IS NOT VERIFIED: THERE IS A PROBLEM IN VERIFYING THE ACCOUNT VIA MOBILE NUMBER IN SERP Website
            # actions.append(SearchActivitiesAction)
            actions.append(RecommendActivitiesAction)
        return actions

    def _execute_actions(self, actions):
        for action_ in actions:
            result = action_().execute(self._state)
            if action_.type == ActionType.AGENT_RESPONSE:
                return result
            elif action_.type == ActionType.STATE_ACTION:
                self._state = result

    def execute(self, user_message):
        self._state.message_history.append({"role": "user", "content": user_message})
        actions = self._decision_making()
        agent_response = self._execute_actions(actions)
        self._state.message_history.append({"role": "assistant", "content": agent_response})
        return agent_response
