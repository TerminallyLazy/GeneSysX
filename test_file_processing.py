import gradio_client
import os
import logging
from gradio_client.exceptions import AppError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_file_processing_and_qa():
    try:
        client = gradio_client.Client('https://02910c43ac5541ad74.gradio.live')
        logger.info('Successfully connected to Gradio client')
    except Exception as e:
        logger.error(f'Failed to connect to Gradio client: {str(e)}', exc_info=True)
        return

    test_file = '/home/ubuntu/GeneSysX/test_sequences.fasta'
    test_pdb_file = '/home/ubuntu/GeneSysX/sample.pdb'

    if not os.path.exists(test_file):
        logger.error(f'Test file {test_file} does not exist.')
        return

    try:
        # Read file content
        with open(test_file, 'r') as f:
            file_content = f.read()
        logger.info(f'Read file content, length: {len(file_content)} characters')

        # Prepare file input as a FileData object
        file_input = gradio_client.FileData(
            path=test_file,
            name=os.path.basename(test_file),
            size=os.path.getsize(test_file),
            data=file_content
        )

        # Send file input as a dictionary
        logger.info(f'Attempting to process file: {test_file}')
        try:
            result = client.predict(
                file_input,  # Send file input as dictionary
                api_name='/process_file_wrapper'
            )
            logger.info(f'File processing result: {result}')
        except Exception as e:
            logger.error(f'Error during file processing: {str(e)}', exc_info=True)

        # Use the same file_input for subsequent API calls

        # Test question answering
        question = "What are the sequence IDs in the uploaded FASTA file?"
        logger.info(f'Attempting to answer question: {question}')
        try:
            qa_result = client.predict(
                question,
                file_input,  # Send file input as dictionary
                api_name='/answer_question_wrapper'
            )
            logger.info(f'Question answering result: {qa_result}')
        except Exception as e:
            logger.error(f'Error during question answering: {str(e)}', exc_info=True)

        # Test multiple sequence alignment
        msa_question = "Perform a multiple sequence alignment"
        logger.info(f'Attempting multiple sequence alignment: {msa_question}')
        try:
            msa_result = client.predict(
                msa_question,
                file_input,  # Send file input as dictionary
                api_name='/answer_question_wrapper'
            )
            logger.info(f'Multiple sequence alignment result: {msa_result}')
        except Exception as e:
            logger.error(f'Error during multiple sequence alignment: {str(e)}', exc_info=True)

        # Test protein visualization
        if os.path.exists(test_pdb_file):
            with open(test_pdb_file, 'r') as f:
                pdb_content = f.read()
            pdb_input = gradio_client.FileData(
                path=test_pdb_file,
                name=os.path.basename(test_pdb_file),
                size=os.path.getsize(test_pdb_file),
                data=pdb_content
            )
            logger.info(f'Attempting protein visualization: {test_pdb_file}')
            try:
                vis_result = client.predict(
                    pdb_input,
                    'white',  # bg_color
                    'cartoon',  # style
                    True,  # spin
                    api_name='/visualize_protein_wrapper'
                )
                logger.info(f'Protein visualization result: {vis_result}')
            except Exception as e:
                logger.error(f'Error during protein visualization: {str(e)}', exc_info=True)
        else:
            logger.warning(f'PDB file {test_pdb_file} not found. Skipping protein visualization test.')

    except AppError as e:
        logger.error(f'Gradio API error: {str(e)}', exc_info=True)
    except AttributeError as e:
        logger.error(f'Attribute error (possibly due to client version mismatch): {str(e)}', exc_info=True)
    except ValueError as e:
        logger.error(f'Value error (possibly due to incorrect API usage): {str(e)}', exc_info=True)
    except TypeError as e:
        logger.error(f'Type error (possibly due to incorrect data type): {str(e)}', exc_info=True)
    except FileNotFoundError as e:
        logger.error(f'File not found error: {str(e)}', exc_info=True)
    except IOError as e:
        logger.error(f'IO error (possibly due to file read/write issues): {str(e)}', exc_info=True)
    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}', exc_info=True)
    finally:
        logger.info('Test completed.')

if __name__ == "__main__":
    test_file_processing_and_qa()
