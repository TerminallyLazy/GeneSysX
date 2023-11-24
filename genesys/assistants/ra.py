from openai import OpenAI
import time
import json
from genesys.env import load_dotenv
import genesys.tools.pubmed as pubmed_tools
import inspect

load_dotenv()

class ResearchAssistant:
    def __init__(self, api_key, model="gpt-4-1106-preview"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_assistant(self, assistant_name, instructions, tools_list):
        assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=instructions,
            tools=tools_list,
            model=self.model
        )
        return assistant

    def initialize_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def run_assistant(self, thread_id, assistant_id, user_input, thread_instructions):
        self.client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
        run = self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions=thread_instructions)
        self.check_run_status(thread_id, run.id)

    def check_run_status(self, thread_id, run_id):
        while True:
            time.sleep(5)
            run_status = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

            if run_status.status == 'completed':
                messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    print(f"{role.capitalize()}: {content}")
                break
            elif run_status.status == 'requires_action':
                self.process_required_actions(thread_id, run_id, run_status.required_action.submit_tool_outputs.model_dump())
            else:
                print("Waiting for the Assistant to process...")
        
    def build_function_map(self):
        function_map = {}
        for name, func in inspect.getmembers(pubmed_tools, inspect.isfunction):
            function_map[name] = func
        return function_map


    def process_required_actions(self, thread_id, run_id, required_actions):
        tool_outputs = []
        function_map = self.build_function_map()

        for action in required_actions["tool_calls"]:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])

            if func_name in function_map:
                function_to_call = function_map[func_name]
                output = function_to_call(**arguments)
                output_str = json.dumps(output)
                tool_outputs.append({
                    "tool_call_id": action['id'],
                    "output": output_str
                })
            else:
                raise ValueError(f"Unknown function: {func_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs)