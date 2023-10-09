import os
import openai
from genesys import ai

TEST_DATA_DIR = "tests/fixtures"

def question_about_file(question, path):
    messages = [
        { "role": "system", "content": ai.system_prompt },
        {
            "role": "user",
            "content": f"""
                {question}

                '{path}'
            """
        }
    ]

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=ai.functions,
        function_call="auto",  # The model decides whether to call a function,
        temperature=0.3,
    )

def test_ask_sequence_type():
    response = question_about_file(
        "What type of sequences are in this file?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "sequence_type"

def test_ask_count_nucleotides():
    pass
