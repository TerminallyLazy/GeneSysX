from genesys.ai import run_conversation
import logging
import os
from io import StringIO

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_test_fasta(file_path):
    with open(file_path, 'w') as f:
        f.write(""">Sequence1
ATGCATGCATGC
>Sequence2
GCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCC
""")

def test_run_conversation():
    # Test case 1: Using file path
    file_path = '/tmp/test_fasta.fasta'
    if not os.path.exists(file_path):
        logging.warning(f"Test file not found at {file_path}. Creating a new test file.")
        create_test_fasta(file_path)

    try:
        result = run_conversation('What are the sequence IDs in the uploaded FASTA file?', file_path, timeout=30)
        print(f"Result (file path): {result}")
    except Exception as e:
        logging.error(f"Error occurred (file path): {str(e)}")

    # Test case 2: Using StringIO
    test_fasta_content = """>Sequence1
ATGCATGCATGC
>Sequence2
GCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCC
"""
    file_input = StringIO(test_fasta_content)

    try:
        result = run_conversation('What are the sequence IDs in the uploaded FASTA file?', file_input, timeout=30)
        print(f"Result (StringIO): {result}")
    except Exception as e:
        logging.error(f"Error occurred (StringIO): {str(e)}")

if __name__ == "__main__":
    test_run_conversation()
