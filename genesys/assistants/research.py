import openai
from openai import OpenAI
import os
import time
from genesys.env import load_dotenv
from genesys.tools import pubmed

load_dotenv()

tools = [{
    "name": "fetch_papers",
    "description": "Fetch papers from PubMed based on a query",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query string used to search for papers in PubMed"
            },
            "max_results": {
                "type": "integer",
                "description": "The maximum number of results to fetch (default is 10)"
            }
        },
        "required": [
            "query"
        ],
        "default": {
            "max_results": 10
        }
    }
}]

# Step 1: init client and assitant
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)

assistant = client.beta.assistants.create(
    name="Research Assistant",
    instructions="You are a research assistant. Your job is to help your boss find papers on PubMed.",
    tools=tools,
    model="gpt-4-1106-preview"
)

# Step 2: create thread
thread = client.beta.threads.create()

# Step 3: append message to thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Can find me papers on FMR1?"
)

# Step 4: run the api

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Papi."
)

print(run.model_dump_json(indent=4))

while True:
    time.sleep(5)
    
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    print(run_status.model_dump_json(indent=4))

    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        # Print all msgs if status is completed
        for msg in messages.data:
            role = msg.role
            content = msg.content[0].text.value
            print(f"{role}: {content}")
        break
    else:
        print("Waiting for completion...")
        time.sleep(5)