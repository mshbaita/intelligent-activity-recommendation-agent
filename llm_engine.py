import os
from abc import abstractmethod, ABC
from typing import List

import openai


class BaseLLM(ABC):
    def __init__(self):
        self._validate_environment()

    @abstractmethod
    def _validate_environment(self):
        raise NotImplementedError


class OpenAILLM(BaseLLM):

    def _validate_environment(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise Exception("No OpenAI API key found")

    def __call__(self, prompt: str, model: str = "text-davinci-003", **kwargs):
        response = openai.Completion.create(
            prompt=prompt,
            model=model,
            **kwargs
        )
        return response.choices[0].text


class OpenAIChatLLM(BaseLLM):

    def _validate_environment(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise Exception("No OpenAI API key found")

    def __call__(self, messages: List[dict], model: str = "gpt-3.5-turbo", **kwargs):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
