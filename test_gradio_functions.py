from gradio_client import Client
import os
import logging
import pkg_resources
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_gradio_version():
    try:
        gradio_version = pkg_resources.get_distribution("gradio").version
        logger.info(f"Gradio version: {gradio_version}")
    except pkg_resources.DistributionNotFound:
        logger.error("Gradio is not installed")

def test_gradio_functions():
    try:
        check_gradio_version()
        client = Client('https://d3707c7667c01f1142.gradio.live')
        logger.info("Successfully connected to Gradio client")

        # Test file processing
        test_file_path = '/home/ubuntu/GeneSysX/test_sequences.fasta'
        if not os.path.exists(test_file_path):
            with open(test_file_path, 'w') as f:
                f.write('>Sequence1\nATCG\n>Sequence2\nGCTA')
            logger.info(f"Created test file: {test_file_path}")

        # Read file content
        with open(test_file_path, 'r') as f:
            file_content = f.read()

        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.fasta', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        # Process file
        try:
            logger.info(f"Sending file: {temp_file_path}")
            result = client.predict(
                temp_file_path,
                api_name="/process_file"
            )
            logger.info(f'File processing result: {result}')
        except Exception as e:
            logger.error(f"Error in file processing: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")

        # Test question answering
        question = 'What are the sequence ids in the uploaded fasta file?'
        try:
            logger.info(f"Sending question: {question}")
            result = client.predict(
                temp_file_path,
                question,
                api_name="/answer_question"
            )
            logger.info(f'Question answering result: {result}')
        except Exception as e:
            logger.error(f"Error in question answering: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")

        # Test protein visualization
        try:
            logger.info("Testing protein visualization")
            pdb_file_path = '/home/ubuntu/GeneSysX/sample.pdb'
            if not os.path.exists(pdb_file_path):
                logger.warning(f"PDB file not found: {pdb_file_path}")
            else:
                result = client.predict(
                    pdb_file_path,
                    'cartoon',
                    True,
                    api_name="/visualize_protein"
                )
                logger.info(f'Protein visualization result: {result[:100]}...')  # Log first 100 characters
        except Exception as e:
            logger.error(f"Error in protein visualization: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")

        # Clean up temporary file
        os.unlink(temp_file_path)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error args: {e.args}")

if __name__ == "__main__":
    test_gradio_functions()
