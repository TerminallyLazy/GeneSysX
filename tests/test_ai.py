"""
This testing module is to make sure that the prompts and the function
descriptions defined in `genesys.ai` results in the behavior that we expect.
"""

import os
import pytest
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
    response = question_about_file(
        "How many nucleotides are in the first sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "count_occurences"

def test_ask_multiple_sequence_alignment():
    response = question_about_file(
        "Perform MSA on the given sequence?",
        os.path.join(TEST_DATA_DIR, "msa.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "multiple_sequence_alignment"


def test_ask_transcription():
    response = question_about_file(
        "What is the mRNA transcript of the given seq?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "transcription"

def test_ask_translation():
    response = question_about_file(
        "What is the amino acid sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "translation"

def test_ask_iso_electric_point():
    response = question_about_file(
        "What is the isoelectric point of the given protein sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "isoelectric_point"

def test_ask_mass_calculator():
    response = question_about_file(
        "What is the molecular weight of the given protein sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "mass_calculator"

def test_ask_restriction_enzyme():
    response = question_about_file(
        "What are the restriction sites in the given sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "restriction_sites"

def test_ask_gc_content():
    response = question_about_file(
        "What is the GC content of the third sequence?",
        os.path.join(TEST_DATA_DIR, "sequence.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "gc_content"

def test_ask_orf():
    response = question_about_file(
        "What are the open reading frames in the given sequence?",
        os.path.join(TEST_DATA_DIR, "random_dna.fasta")
    )
    response_message = response["choices"][0]["message"]
    assert response_message.get("function_call")
    assert response_message["function_call"]["name"] == "open_reading_frames"

@pytest.mark.skip(reason="used for manual testing")
def test_run_conversation():
    filepath = os.path.join(TEST_DATA_DIR, "sequence.fasta")
    print(ai.run_conversation("What type of sequences are in this file?", filepath))
