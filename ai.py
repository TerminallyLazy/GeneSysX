import openai
import json
from DNAToolKit import transcription, countNucleotides
from fasta_2_string import fasta_to_string
from API_SECRETS import OPEN_API_KEY

openai.api_key = OPEN_API_KEY

fasta_file = "sequence.fasta"
sequences_as_string = fasta_to_string(fasta_file)


user_input = input("Hi! Enter your request: ")

def run_conversation():
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
                    "rna": {
                        "type": "string",
                        "description": "The RNA sequence to transcribe",
                    },
                },
                "required": ["rna"],
            },
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
            "countNucleotides": countNucleotides
        }
        
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)

        if function_to_call is not None:
            function_args = json.loads(response_message["function_call"]["arguments"])
            if function_name == "countNucleotides":
                function_response = function_to_call(
                    dna=function_args.get("dna"),
                )
            else:
                function_response = function_to_call(
                    rna=function_args.get("rna"),
                    )

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

# Run the conversation and get the response
print(run_conversation())
