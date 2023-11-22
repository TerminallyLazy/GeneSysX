import json
from types import ModuleType
from typing import NotRequired, Unpack

from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_create_params import AssistantCreateParams
from openai.types.beta.threads.run import Run

from ..utils import gen_tools_schema
from ..openai import openai_client

DEFAULT_MODEL = "gpt-4-1106-preview"

class _BaseAssistantCreateParams(AssistantCreateParams):
    model: NotRequired[str]

def create_base_assistant(**kwargs: Unpack[_BaseAssistantCreateParams]) -> Assistant:
    kwargs.setdefault("model", DEFAULT_MODEL)
    return openai_client.beta.assistants.create(**kwargs)

class BaseAssistant:
    model = "gpt-4-1106-preview"

    def __init__(self, tools_module: ModuleType, **kwargs: Unpack[_BaseAssistantCreateParams]):
        self.tools = tools_module.__dict__
        kwargs.setdefault("model", self.model)
        self.assistant = create_base_assistant(**kwargs)
        
    def __getattr__(self, name: str) -> Assistant:
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
        return openai_client.beta.assistants.delete(self.assistant.id)

    # HACK: AssistantCreateParams and AssistantUpdateParams are the same
    def update(self, **kwargs: Unpack[_BaseAssistantCreateParams]) -> Assistant:
        return openai_client.beta.assistants.update(**kwargs)

    def get_tool_outputs(self, run: Run):
        tool_outputs = []
        
        for action in run.required_action.submit_tool_outputs.tool_calls:
            if (fn_name := action.function.name) in self.tools:
                function_to_call = self.tools[fn_name]
                args = json.loads(action.function.arguments)
                ret = function_to_call(**args)
                tool_outputs.append({
                    "tool_call_id": action.id,
                    "output": json.dumps(ret)
                })
            else:
                raise ValueError(f"Unknown tool: {fn_name}")
                
        return tool_outputs
            