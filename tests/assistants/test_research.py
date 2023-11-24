import pytest
import time
from genesys.openai import openai_client as client
from genesys.assistants import research_assistant
from genesys.assistants.ra import *


def test_assistant_conversation():

    run = client.beta.threads.create_and_run(
        assistant_id=research_assistant.id,
        thread={
            "messages": [
                {"role": "user",
                 "content": "Can you get me papers about FMR1?"}
            ]
        }
    )

    while True:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            run_id=run.id, thread_id=run.thread_id)

        if run.status == "requires_action" and run.required_action is not None:
            tool_outputs = research_assistant.get_tool_outputs(run)
            res = client.beta.threads.runs.submit_tool_outputs(
                run_id=run.id, thread_id=run.thread_id, tool_outputs=tool_outputs)
        elif run.status == "completed":
            break

    # Retrieve and assert messages
    messages = client.beta.threads.messages.list(thread_id=run.thread_id)
    assert run.status == "completed"


def test_ra_create_assistant():
    pass