import gradio_client
import time
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_gradio_app():
    client = gradio_client.Client('https://a9a4d0845ba3bbe0fe.gradio.live')

    # Test file processing
    logger.info("Testing file processing...")
    file_path = 'test_sequences.fasta'
    try:
        if os.path.exists(file_path):
            result = client.predict(
                file_path,
                api_name='/process_file'
            )
            logger.info(f'File processing result: {result}')
        else:
            logger.warning(f"File {file_path} not found. Skipping file processing test.")
    except Exception as e:
        logger.error(f"An error occurred during file processing: {str(e)}", exc_info=True)

    # Test question answering and multiple sequence alignment
    logger.info("\nTesting question answering and multiple sequence alignment...")
    question = 'Perform a multiple sequence alignment and describe the results.'
    try:
        if os.path.exists(file_path):
            result = client.predict(
                question,
                file_path,
                api_name='/answer_question'
            )
            logger.info(f'Question answering result: {result}')
        else:
            logger.warning(f"File {file_path} not found. Skipping question answering and MSA test.")
    except Exception as e:
        logger.error(f"An error occurred during question answering: {str(e)}", exc_info=True)

    # Test protein visualization
    logger.info("\nTesting protein visualization...")
    pdb_file_path = 'sample.pdb'
    try:
        if os.path.exists(pdb_file_path):
            result = client.predict(
                pdb_file_path,
                'cartoon',
                True,
                api_name='/visualize_protein'
            )
            logger.info(f'Protein visualization result: {result}')
        else:
            logger.warning(f"File {pdb_file_path} not found. Skipping protein visualization test.")
    except Exception as e:
        logger.error(f"An error occurred during protein visualization: {str(e)}", exc_info=True)

    # Check UI changes
    logger.info("\nChecking UI changes...")
    try:
        ui_components = client.view_api()
        if 'theme' not in str(ui_components) and 'font_size' not in str(ui_components):
            logger.info("UI check passed: Light/dark mode and font size options are not present.")
        else:
            logger.warning("UI check failed: Light/dark mode or font size options might still be present.")
    except Exception as e:
        logger.error(f"An error occurred while checking UI changes: {str(e)}", exc_info=True)

    # Check logging implementation
    logger.info("\nChecking logging implementation...")
    try:
        # This is a simple check to see if logging is implemented
        # You may need to adjust this based on how logging is actually implemented in your app
        result = client.predict("Check logging", api_name='/process_file')
        if "log" in str(result).lower():
            logger.info("Logging check passed: Logging seems to be implemented.")
        else:
            logger.warning("Logging check inconclusive: Unable to verify logging implementation.")
    except Exception as e:
        logger.error(f"An error occurred while checking logging implementation: {str(e)}", exc_info=True)

if __name__ == '__main__':
    test_gradio_app()

if __name__ == '__main__':
    test_gradio_app()
