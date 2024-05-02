from abc import abstractmethod


class State:

    def __init__(self):
        self.required_slots = {
            "num_adults": None,
            "ages_of_adults": None,
            "gender_of_adults": None,
            "num_children": None,
            "ages_of_children": None,
            "gender_of_children": None,
            "location": None,
            "interests": None
        }
        self.optional_slots = {
            "start_date": None,
            "end_date": None
        }
        self.message_history = list()

        self.search_result = ""

    @abstractmethod
    def get_destination(self):
        return self.required_slots.get("location", "")
