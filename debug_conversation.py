import logging
import os
from io import StringIO
logging.basicConfig(level=logging.DEBUG)
from genesys.ai import run_conversation

def create_test_fasta(file_path):
    with open(file_path, 'w') as f:
        f.write(""">Sequence1
ATGCATGCATGC
>Sequence2
GCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCC
""")

def debug_run_conversation():
    question = 'What are the sequence IDs in the uploaded FASTA file?'
    file_path = '/tmp/gradio/830786ed162059d66bc9bb17217ca8f87f118e506102ee5213a93c77ff64ee7e/sample.fasta'

    # Create test file if it doesn't exist
    if not os.path.exists(file_path):
        logging.warning(f"Test file not found at {file_path}. Creating a new test file.")
        create_test_fasta(file_path)

    print('Debug: Starting run_conversation with file path')
    try:
        result = run_conversation(question, file_path, timeout=30)
        print(f'Debug: Result from run_conversation (file path): {result}')
    except Exception as e:
        print(f'Debug: Error occurred during run_conversation (file path): {str(e)}')

    # Test with StringIO
    test_fasta_content = """>Sequence1
ATGCATGCATGC
>Sequence2
GCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCC
"""
    file_input = StringIO(test_fasta_content)

    print('Debug: Starting run_conversation with StringIO')
    try:
        result = run_conversation(question, file_input, timeout=30)
        print(f'Debug: Result from run_conversation (StringIO): {result}')
    except Exception as e:
        print(f'Debug: Error occurred during run_conversation (StringIO): {str(e)}')

if __name__ == "__main__":
    debug_run_conversation()
