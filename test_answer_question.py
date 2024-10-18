import gradio as gr
from app import answer_question, process_file
from io import StringIO
import logging
import os
import tempfile

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_fasta(file_path):
    content = """>Sequence1
ATGCATGCATGCATGCATGCATGC
>Sequence2
GCTAGCTAGCTAGCTAGCTAGCTA
>Sequence3
AAAAGGGGCCCCTTTTAAAACCCC
"""
    with open(file_path, 'w') as f:
        f.write(content)
    return content

def test_answer_question():
    # Test with a NamedString object
    class NamedString(StringIO):
        def __init__(self, content, name):
            super().__init__(content)
            self.name = name

    named_string = NamedString(">Sequence1\nATCG\n>Sequence2\nGCTA", "test.fasta")

    # Create a temporary test FASTA file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.fasta') as temp_file:
        test_fasta_content = create_test_fasta(temp_file.name)
        temp_file_path = temp_file.name

    # Test cases
    test_cases = [
        (named_string, "What are the sequence ids in the uploaded fasta file?"),
        (gr.File(temp_file_path), "Perform a multiple sequence alignment"),
        ({"name": "test.fasta", "content": test_fasta_content}, "What is the GC content?"),
        (temp_file_path, "How many sequences are in the file?")
    ]

    for file_input, question in test_cases:
        logger.info(f"Testing with question: {question}")
        logger.info(f"File input type: {type(file_input)}")

        try:
            if isinstance(file_input, gr.File):
                logger.info(f"gr.File object details:")
                logger.info(f"  Type: {type(file_input)}")
                logger.info(f"  Attributes: {dir(file_input)}")
                logger.info(f"  Value: {file_input.value}")
                logger.info(f"  Name: {getattr(file_input, 'name', 'N/A')}")
                if hasattr(file_input, 'file'):
                    logger.info(f"  File attribute: {file_input.file}")
                    if hasattr(file_input.file, 'name'):
                        logger.info(f"  File name: {file_input.file.name}")

            # Process the file
            processed_result = process_file(file_input)
            logger.info(f"Processed result: {processed_result}")

            if processed_result['status'] == 'error':
                logger.error(f"Error in process_file: {processed_result['message']}")
                continue

            # Call answer_question function
            result = answer_question(question, file_input)
            logger.info(f"Question: {question}")
            logger.info(f"Result: {result}")

            # Check for expected content in the answer
            if "sequence ids" in question.lower():
                expected_ids = ["Sequence1", "Sequence2", "Sequence3"]
                if all(seq_id in result for seq_id in expected_ids):
                    logger.info("All expected sequence IDs found in the answer.")
                else:
                    logger.warning("Not all expected sequence IDs found in the answer.")
            elif "gc content" in question.lower():
                if "%" in result:
                    logger.info("GC content percentage found in the answer.")
                else:
                    logger.warning("GC content percentage not found in the answer.")
            elif "how many sequences" in question.lower():
                if "3" in result:
                    logger.info("Correct number of sequences found in the answer.")
                else:
                    logger.warning("Correct number of sequences not found in the answer.")

            logger.info("---")
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            logger.info("---")

    # Clean up the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        logger.info(f"Temporary file {temp_file_path} removed.")

if __name__ == "__main__":
    test_answer_question()
