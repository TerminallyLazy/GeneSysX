import os
import json
import openai
from openai import OpenAI
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
    import logging
    import os
    from io import StringIO
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Starting run_conversation with user_input: {user_input}, fasta_file: {fasta_file}")

    # Check if fasta_file is a StringIO object or a file path
    if isinstance(fasta_file, StringIO):
        content = fasta_file.getvalue()[:100]
        filepath = "memory_file.fasta"  # Placeholder name for StringIO objects
        logging.debug(f"First 100 characters of StringIO content: {content}")
    elif os.path.exists(fasta_file):
        try:
            with open(fasta_file, 'r') as f:
                content = f.read(100)
                logging.debug(f"First 100 characters of file content: {content}")
            filepath = fasta_file
        except IOError as e:
            logging.error(f"Error reading file: {str(e)}")
            return f"An error occurred: {str(e)}"
    else:
        logging.error(f"File does not exist: {fasta_file}")
        return "Error: File does not exist"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Step 1: Send the user query and available functions to GPT-4
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""
                {user_input}

                '{filepath}'
                """
        }
    ]

    try:
        # Step 2: Get the initial response from GPT-4
        logging.info("Sending initial request to GPT-4")
        response = client.chat.completions.create(
            model="gpt-4",  # Use the correct model name
            messages=messages,
            functions=functions,
            function_call="auto",
            temperature=0.3,
        )
        logging.debug(f"Received initial response: {response}")

        response_message = response.choices[0].message
        logging.info(f"Response message: {response_message}")

        # Step 3: Check if GPT wants to call a function
        if response_message.function_call:
            function_name = response_message.function_call.name
            logging.info(f"GPT wants to call function: {function_name}")

            if function_name is not None:
                try:
                    function_to_call = getattr(toolkit, function_name)
                    function_args = json.loads(response_message.function_call.arguments)
                    motif = function_args.get("motif", None)
                    logging.info(f"Calling function {function_name} with filepath: {filepath}, motif: {motif}")

                    if isinstance(fasta_file, StringIO):
                        if function_name == "find_motifs":
                            function_response = function_to_call(filepath=fasta_file.getvalue(), motif=motif)
                        else:
                            function_response = function_to_call(filepath=fasta_file.getvalue())
                    else:
                        if function_name == "find_motifs":
                            function_response = function_to_call(filepath=filepath, motif=motif)
                        else:
                            function_response = function_to_call(filepath=filepath)
                    logging.debug(f"Function response: {function_response}")

                    # Step 4: Extend the conversation with the function call and response
                    messages.append(response_message)
                    messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": str(function_response),
                        }
                    )

                except (json.JSONDecodeError, AttributeError) as e:
                    logging.error(f"Error calling function: {str(e)}")
                    function_response = f"An error occurred: {str(e)}"
                    messages.append(
                        {
                            "role": "function",
                            "name": "error",
                            "content": function_response,
                        }
                    )

        # Step 5: Send the extended conversation to GPT for further interaction
        logging.info("Sending second request to GPT-4")
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
        )
        logging.debug(f"Received second response: {second_response}")

        answer = second_response.choices[0].message.content
        logging.info(f"Final answer: {answer}")
        return answer

    except Exception as e:
        logging.error(f"An error occurred in run_conversation: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}"
