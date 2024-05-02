from copy import deepcopy

from actions.base import BaseAction, ActionType
from llm_engine import OpenAIChatLLM
from state import State
from datetime import date


class SlotsExtractionAction(BaseAction):

    name = "SLOTS_EXTRACTION"
    type = ActionType.STATE_ACTION
    PROMPT_TEMPLATE = """
You are an AI assistant trained to perform slot extraction. In this task, your goal is to extract relevant slots from their messages and to map it to the provided required and optional slots. Please provide the extracted slots as your response without generating additional text.

Please make sure to explicitly provide any necessary slot values in your responses.

Parse the user's message and extract intents and slots.
If any date or time extracted, provide them in python format, today is {today}.
The output should be only new-line-seperated key: value pairs, no json, no other tokens.
If a value is provided in the required slots but not explicitly mentioned in the user messages, don't extract it in your response.
DO NOT INCLUDE EMPTY VALUES INSIDE YOUR OUTPUT SUCH AS not provided when user is not providing such information
Output format should be in the following format:
<required_slot_1>: <extracted_value_1>
<required_slot_2>: <extracted_value_2>

Required slots:
{required_slots}
    """.strip()

    def __init__(self):
        self._chat_llm = OpenAIChatLLM()

    def _get_messages(self, state):
        required_info = ""
        optional_info = ""

        for key, value in state.required_slots.items():
            required_info += f"{key}: {value or ' '}"
            required_info += "\n"
        for key, value in state.optional_slots.items():
            optional_info += f"{key}: {value or ' '}"
            optional_info += "\n"

        ner_prompt = self.PROMPT_TEMPLATE.format(
            required_slots=required_info,
            optional_slots=optional_info,
            today=str(date.today())
        )
        messages = deepcopy(state.message_history)
        messages.append({"role": "system", "content": ner_prompt})
        return messages

    @staticmethod
    def _update_state(state, result):
        new_state = deepcopy(state)
        for line_ in result.split("\n"):
            line_ = line_.strip()
            try:
                line_kv = line_.split(":")
                key_ = line_kv[0].strip()
                value_ = line_kv[1].strip()

                if not value_:
                    continue

                if key_ in new_state.required_slots.keys():
                    new_state.required_slots[key_] = value_
                elif key_ in new_state.optional_slots.keys():
                    new_state.optional_slots[key_] = value_
                else:
                    raise Exception(f"key started not valid, key {key_}")
            except Exception as e:
                print(f"skipping line {line_}, error: {repr(e)}")
        return new_state

    def execute(self, state: State):
        messages_ = self._get_messages(state)
        result = self._chat_llm(messages=messages_, temperature=0.0)
        # print(f"nlu_result:\n{result}")
        new_state = SlotsExtractionAction._update_state(state, result)
        print(f"new_state.required_slots:\n{new_state.required_slots}")
        print(f"new_state.optional_slots:\n{new_state.optional_slots}")
        return new_state
