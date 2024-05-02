from copy import deepcopy

from actions.base import BaseAction, ActionType
from google_engine import GoogleSearch
from state import State


class SearchActivitiesAction(BaseAction):
    name = "SEARCH_ACTIVITIES"
    type = ActionType.STATE_ACTION

    def __init__(self):
        self.google_search = GoogleSearch()

    @staticmethod
    def __update_state(state: State, search_result):
        new_state = deepcopy(state)
        new_state.search_result = search_result
        return new_state

    def execute(self, state: State):
        query_result = self.google_search(query=f"What kind of activities can be done in {state.get_destination()}")
        new_state = SearchActivitiesAction.__update_state(state, query_result)
        return new_state
