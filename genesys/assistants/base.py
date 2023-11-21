from typing import NotRequired, Unpack

from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_create_params import AssistantCreateParams

from ..openai import openai_client

DEFAULT_MODEL = "gpt-4-1106-preview"

class _BaseAssistantCreateParams(AssistantCreateParams):
    model: NotRequired[str]

def create_base_assistant(**kwargs: Unpack[_BaseAssistantCreateParams]) -> Assistant:
    kwargs.setdefault("model", DEFAULT_MODEL)
    return openai_client.beta.assistants.create(**kwargs)
