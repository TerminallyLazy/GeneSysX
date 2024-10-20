import os
import json
import openai
from . import eventcreator as ec
from . import DNAToolKit as toolkit
from .env import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = "Be a bioinformatician who answers questions about a FASTA file with the given path."

functions = [
    {
        "name": "sequence_type",
        "description": "Get the type of sequences in a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                }
            },
            "required": ["filepath"]
        },
        "returns": {
            "type": "object",
            "properties": {
                "sequence_type": {
                    "type": "string",
                    "enum": ["DNA", "RNA", "Protein"],
                }
            },
        }
    },
    {
        "name": "count_occurences",
        "description": "Count the number of nucleotides for each DNA/RNA sequence or amino acids for each protein in a FASTA file",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "transcription",
        "description": "Transcribe a DNA sequence to RNA.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "complementary",
        "description": "Find the complementary DNA sequence to a given DNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "reverseComplementary",
        "description": "Find the reverse complementary of a sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "gc_content",
        "description": "Calculate the GC content of a DNA/RNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "translation",
        "description": "Translate a DNA sequence to a protein sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "mass_calculator",
        "description": "Calculate the molecular mass of a DNA, RNA or protein sequence",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "restriction_sites",
        "description": "Find the restriction sites of a DNA sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "isoelectric_point",
        "description": "Calculate the isoelectric point of a protein sequence.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The protein sequence."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "multiple_sequence_alignment",
        "description": "Perform multiple sequence alignment using a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the FASTA file."
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "construct_phylogenetic_tree",
        "description": "Construct a phylogenetic tree using a FASTA file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "open_reading_frames",
        "description": "Finds the forward and reverse open reading frames",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "detect_snps",
        "description": "Detect single nucleotide polymorphisms (SNPs)",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
            },
            "required": ["filepath"]
        },
    },
    {
        "name": "find_motifs",
        "description": "Find motifs in a DNA sequence",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                },
                "motif": {
                    "type": "string",
                }
            },
            "required": ["filepath", "motif"]
        }
    }
]

def run_conversation(user_input, fasta_file):
    # Step 1: Send the user query and available functions to GPT-3.5 Turbo
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""
                {user_input}

                '{fasta_file}'
                """
        }
    ]

from openai import OpenAI

client = OpenAI()

def create_chat_completion(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        # functions=functions,
        function_call="auto",  # The model decides whether to call a function
        temperature=0.3,
    )
    return response
#     temperature=0.3,
# )

# def create_chat_completion(user_input):
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_input}
#         ],
#         #functions=functions,
#         function_call="auto",  # The model decides whether to call a function
#         temperature=0.3,
#     )
    #return response

    response_message = response.choices[0].message
    # ec.create_response_event(username, current_session, response_message)

    # Initialize function_response with a default value
    function_response = None

    # Step 2: Check if GPT wants to call a function
    if response_message.function_call:
        # Step 3: Call the function based on the model's response
        function_name = response_message.function_call.name

        if function_name is not None:
            try:
                function_to_call = getattr(toolkit, function_name)
                function_args = json.loads(response_message.function_call.arguments)
                filepath = function_args.get("filepath")
                motif = function_args.get("motif", None)

                if function_name == "find_motifs":
                    function_response = function_to_call(filepath=filepath, motif=motif)
                else:
                    function_response = function_to_call(filepath=filepath) 

            except json.JSONDecodeError:
                function_response = "An error occurred while decoding the function arguments."
    
    # Step 4: Extend the conversation with the function call and response
    # Extend the conversation with the assistant's reply
    if 'messages' not in locals():
        messages = []
    messages.append(response_message)
    if function_response is not None:
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            }
        )  # Extend the conversation with the function response

    # Step 5: Send the extended conversation to GPT for further interaction
    second_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    answer = second_response.choices[0].message.content
    # ec.create_response_event(username, current_session, answer)

    return answer
