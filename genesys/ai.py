import openai
import json
from DNAToolKit import *
from tabular_mods import *
from API_SECRETS import OPEN_API_KEY

openai.api_key = OPEN_API_KEY

def run_conversation(user_input, sequences_as_string):
    # Step 1: Send the user query and available functions to GPT-3.5 Turbo
    messages = [{"role": "user", "content": f"Take the user's request {user_input} and perform the respective actions to the following the DNA sequence: {sequences_as_string}"}]
    
    functions = [
        {
            "name": "countNucleotides",
            "description": "Count nucleotides in a DNA sequence",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The DNA sequence to count nucleotides",
                    },
                },
                "required": ["dna"],
            },
        },
        {
            "name": "transcription",
            "description": "Transcribe an RNA sequence to its complementary DNA sequence",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The DNA sequence to transcribe",
                    },
                },
                "required": ["dna"],
            },
        },
        {
            "name": "translation",
            "description": "Translates the sequence to it's protein sequence",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The sequence to be translated",
                    },
                },
                "required": ["dna"],
            },
        },
        {
            "name": "restriction_sites",
            "description": "Finds the restriction sites of a given DNA seq",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The DNA sequence to look at",
                    },
                },
                "required": ["dna"],
            },
            "returns": {
                "type": "string",
                "description": "A string containing the restriction sites found in the DNA sequence.",
            }
        },
        {
            "name": "protein_mass",
            "description": "Calculates the protein mass from the protein sequence",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The DNA sequence to look at",
                    },
                },
                "required": ["dna"],
            },
            "returns": {
                "type": "string",
                "description": "The protein mass found in the DNA sequence.",
            }
        },
        {
            "name": "open_reading_frames",
            "description": "Calculates the open reading frames (ORFs) from a given DNA sequence and translates them into protein sequences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dna": {
                        "type": "string",
                        "description": "The DNA sequence to analyze for open reading frames (ORFs).",
                    }
                },
                "required": ["dna"]
            },
            "returns": {
                "type": "object",
                "description": "An object containing the translated protein sequences derived from the identified open reading frames (ORFs).",
                "properties": {
                    "frame1": {
                        "type": "string",
                        "description": "The protein sequence translated from the first reading frame.",
                    },
                    "frame2": {
                        "type": "string",
                        "description": "The protein sequence translated from the second reading frame.",
                    },
                    "frame3": {
                        "type": "string",
                        "description": "The protein sequence translated from the third reading frame.",
                    }
                }
            }
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # The model decides whether to call a function
    )

    response_message = response["choices"][0]["message"]

    # Step 2: Check if GPT wants to call a function
    if response_message.get("function_call"):
        # Step 3: Call the function based on the model's response
        available_functions = {
            "transcription": transcription,
            "countNucleotides": countNucleotides,
            "restriction_sites": restriction_sites,
            "translation": translation,
            "protein_mass": protein_mass,
            "open_reading_frames": open_reading_frames
        }
        
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)

        if function_to_call is not None:
            try:
                function_args = json.loads(response_message["function_call"]["arguments"])
                if function_name == "countNucleotides":
                    function_response = function_to_call(
                        dna=function_args.get("dna"),
                    )
                elif function_name == "transcription":
                    function_response = function_to_call(
                        dna=function_args.get("dna"),
                    )
                elif function_name == "restriction_sites":
                    function_response = function_to_call(
                        dna=function_args.get("dna"),
                    )
                elif function_name == "translation":
                    function_response = function_to_call(
                        dna=function_args.get("dna")
                    )
                elif function_name == "protein_mass":
                    function_response = function_to_call(
                        dna=function_args.get("dna")
                    )
                elif function_name == "open_reading_frames":
                    function_response = function_to_call(
                        dna=function_args.get("dna")
                    )
                else:
                    function_response = function_to_call(
                        dna=function_args.get("dna"),
                    )
                    

            except json.JSONDecodeError:
                function_response = "An error occurred while decoding the function arguments."

        # Step 4: Extend the conversation with the function call and response
        messages.append(response_message)  # Extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # Extend conversation with function response

        # Step 5: Send the extended conversation to GPT for further interaction
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )

        answer = second_response["choices"][0]["message"]["content"]

        return answer

