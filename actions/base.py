from abc import ABC, abstractmethod
from enum import Enum

from state import State


class ActionType(Enum):
    STATE_ACTION = "STATE_ACTION"
    AGENT_RESPONSE = "AGENT_RESPONSE"
    GOOGLE_SEARCH = "GOOGLE_SEARCH"


class BaseAction(ABC):

    @abstractmethod
    def execute(self, state: State):
        raise NotImplementedError
