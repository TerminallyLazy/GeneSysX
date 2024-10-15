import json
from types import ModuleType
from typing import Optional, TypedDict, Unpack

from openai import OpenAI

DEFAULT_MODEL = "gpt-4"

from typing import Any, TypedDict, Unpack

class AssistantCreateParams(TypedDict):
    model: str


def initialize_base_assistant(**kwargs: Unpack[AssistantCreateParams]) -> Any:
    kwargs['model'] = kwargs.get('model') or DEFAULT_MODEL
    return OpenAI().beta.assistants.create(**kwargs)

class BaseAssistant:
    model: str = DEFAULT_MODEL

    def __init__(self, tools_module: ModuleType, **kwargs: Unpack[AssistantCreateParams]):
        self.tools = tools_module.__dict__
        kwargs.setdefault("model", self.model)
        self.assistant = create_base_assistant(**kwargs)
        self.client = OpenAI()
        
    def __getattr__(self, name: str) -> Any:
        return getattr(self.assistant, name)

    def __repr__(self) -> str:
        return f"<BaseAssistant: {self.assistant.id}>"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseAssistant):
            return NotImplemented
        return self.assistant.id == other.assistant.id

    def __hash__(self) -> int:
        return hash(self.assistant.id)

    def delete(self):
        return self.client.beta.assistants.delete(self.assistant.id)

import openai
from openai.types.beta import AssistantCreateParams
from openai.types.beta import Assistant
from typing import Unpack

def create_base_assistant(**kwargs: Unpack[AssistantCreateParams]) -> Assistant:
    kwargs.setdefault("model", DEFAULT_MODEL)
    return openai.beta.assistants.create(**kwargs)

# def update(self, **kwargs: Unpack[AssistantCreateParams]) -> 'Assistant':
#     return self.client.beta.assistants.update(assistant_id=self.assistant['id'], **kwargs)

def get_tool_outputs(self, run):
        tool_outputs = []
        if run.required_action and run.required_action.type == "submit_tool_outputs":
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if (fn_name := tool_call.function.name) in self.tools:
                    function_to_call = self.tools[fn_name]
                    args = json.loads(tool_call.function.arguments)
                    ret = function_to_call(**args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(ret)
                    })
                else:
                    raise ValueError(f"Unknown tool: {fn_name}")
                
        return tool_outputs