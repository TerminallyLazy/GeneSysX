import os
import json
import openai
from .protein_render import *
from .DNAToolKit import *
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
        "description": "Find the reverse complementary DNA sequence to a given DNA sequence.",
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
        "name": "render_protein_file",
        "description": "Renders a 3D protein file.",
        "parameters": {
            "type": "object",
            "properties": {
                "pdb_file_content": {
                    "type": "string",
                    "description": "The content of the PDB file to render in 3D."
                },
                "style": {
                    "type": "string",
                    "description": "The style to apply to the protein rendering (e.g., 'cartoon').",
                    "default": "cartoon"
                },
            },
            "required": ["pdb_file_content"]
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

    # TODO: extract chat completion options
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # The model decides whether to call a function,
        temperature=0.3,
    )

    response_message = response["choices"][0]["message"]

    # Initialize function_response with a default value
    function_response = None

    # Step 2: Check if GPT wants to call a function
    if response_message.get("function_call"):
        # Step 3: Call the function based on the model's response
        available_functions = {
            "sequence_type": sequence_type,
            "count_occurences": count_occurences,
            "transcription": transcription,
            "complementary": complementary,
            "reverseComplementary": reverseComplementary,
            "gc_content": gc_content,
            "translation": translation,
            "mass_calculator": mass_calculator,
            "restriction_sites": restriction_sites,
            "isoelectric_point": isoelectric_point,
            "render_protein_file": render_protein_file,
        }

        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)

        if function_to_call is not None:
            try:
                function_args = json.loads(
                    response_message["function_call"]["arguments"])
                if function_name == "sequence_type":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "count_occurences":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "transcription":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "complementary":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "reverseComplementary":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "gc_content":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "translation":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "mass_calculator":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "restriction_sites":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "isoelectric_point":
                    function_response = function_to_call(
                        filepath=function_args.get("filepath"),
                    )
                elif function_name == "render_protein_file":
                    function_response = function_to_call(
                        pdb_file_content=function_args.get("pdb_file_content"),
                    )
                else:
                    # Add handling for other functions if needed
                    pass

            except json.JSONDecodeError:
                function_response = "An error occurred while decoding the function arguments."

    # Step 4: Extend the conversation with the function call and response
    # Extend the conversation with the assistant's reply
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
    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )

    answer = second_response["choices"][0]["message"]["content"]

    return answer
