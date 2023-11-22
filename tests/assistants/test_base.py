from genesys.assistants.base import BaseAssistant, create_base_assistant
from genesys.openai import openai_client

def test_create_assistant():
    test_assistant = create_base_assistant(
        name="Test Assistant",
        description="Used for testing.",
        metadata={"test": True}
    )
    also_test_assistant = openai_client.beta.assistants.retrieve(test_assistant.id)
    assert test_assistant.id == also_test_assistant.id

def test_base_assistant_class():
    test_assistant = BaseAssistant(
        name="Test Assistant",
        description="Used for testing.",
        metadata={"test": True}
    )
    also_test_assistant = openai_client.beta.assistants.retrieve(test_assistant.id)
    assert test_assistant.id == also_test_assistant.id