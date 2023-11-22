from .base import BaseAssistant
from ..tools import pubmed
from ..utils import gen_tools_schema


DEFAULT_MODEL = "gpt-4-1106-preview"

research_assistant = BaseAssistant(
    tools_module=pubmed,
    name="Research Assistant",
    description="A research assistant to help you with your work.",
    instructions="Help find sources for my research paper.",
    tools=gen_tools_schema(pubmed),
)

#bioinformatician_assistant = client.beta.assistants.create(
#    model=DEFAULT_MODEL,
#    name="Bioinformatician Assistant",
#    description="A bioinformatician assistant to help you analyze your biological data.",
#    instructions="Help me find the best way to analyze my data.",
#    tools=gen_tools_schema(pubmed),
#)
