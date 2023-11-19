from genesys.assistants.ra import *
import os

literature_tools = [
    {
        "type": "function",
        "function": {
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
                        "description": "The maximum number of results to fetch",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    }
]

assistant = ResearchAssistant(api_key=os.environ['OPENAI_API_KEY'])

user_input_medical = "What are the latest advancements in neurology?"
assistant.create_assistant_and_run(user_input=user_input_medical, assistant_name="Borj",
                                   instructions="Find papers most relevant to my query.", tools_list=literature_tools, thread_instructions="Your output of papers should always be bullet points where the main bullet point is the paper and the sub-bullet points are the abstract and link to the paper.")
