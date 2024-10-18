import logging
import os
from genesys.ai import run_conversation
from io import StringIO
from Bio import SeqIO

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

# Test with a StringIO object containing a sample FASTA content
sample_fasta = StringIO(""">Sequence1
ATGCATGCATGC
>Sequence2
GCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCC
""")

def run_test(input_type, fasta_input, question):
    try:
        result = run_conversation(question, fasta_input)
        logging.info(f"Test with {input_type} - Question: {question}")
        logging.info(f"Result: {result}")
        print(f"\nTest with {input_type} - Question: {question}")
        print(f"Result: {result}\n")
    except Exception as e:
        logging.error(f"Error occurred with {input_type}: {str(e)}")
        print(f"\nError occurred with {input_type}: {str(e)}\n")

# Test with StringIO
run_test("StringIO", sample_fasta, 'What are the sequence IDs in the uploaded FASTA file?')
run_test("StringIO", sample_fasta, 'How many sequences are in the file?')

# Test with file path
file_path = '/tmp/gradio/830786ed162059d66bc9bb17217ca8f87f118e506102ee5213a93c77ff64ee7e/test_fasta.fasta'
if not os.path.exists(file_path):
    logging.warning(f"Test file not found at {file_path}. Creating a new test file.")
    create_test_fasta(file_path)

run_test("File Path", file_path, 'What are the sequence IDs in the uploaded FASTA file?')
run_test("File Path", file_path, 'What is the length of the first sequence?')

# Verify extracted sequence IDs
def verify_sequence_ids(fasta_input):
    if isinstance(fasta_input, StringIO):
        fasta_input.seek(0)
    sequence_ids = [record.id for record in SeqIO.parse(fasta_input, "fasta")]
    logging.info(f"Verified sequence IDs: {sequence_ids}")
    print(f"Verified sequence IDs: {sequence_ids}")

verify_sequence_ids(sample_fasta)
verify_sequence_ids(file_path)
