import gradio_client
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_functionality():
    try:
        client = gradio_client.Client('https://02910c43ac5541ad74.gradio.live')
        logger.info('Successfully connected to Gradio client')

        # View API
        api_info = client.view_api()
        logger.info(f'API Info: {api_info}')

        # Test file processing
        with open('/home/ubuntu/GeneSysX/test_sequences.fasta', 'r') as f:
            file_content = f.read()
        file_input = gradio_client.FileData(
            path='/home/ubuntu/GeneSysX/test_sequences.fasta',
            name='test_sequences.fasta',
            size=len(file_content),
            data=file_content
        )
        result = client.predict(file_input, api_name='/process_file_wrapper')
        logger.info(f'File processing result: {result}')

        # Test Q&A
        question = "What are the sequence IDs in the uploaded FASTA file?"
        qa_result = client.predict(question, file_input, api_name='/answer_question_wrapper')
        logger.info(f'Q&A result: {qa_result}')

        # Test protein visualization
        with open('/home/ubuntu/GeneSysX/sample.pdb', 'r') as f:
            pdb_content = f.read()
        pdb_input = gradio_client.FileData(
            path='/home/ubuntu/GeneSysX/sample.pdb',
            name='sample.pdb',
            size=len(pdb_content),
            data=pdb_content
        )
        vis_result = client.predict(pdb_input, 'white', 'cartoon', True, api_name='/visualize_protein_wrapper')
        logger.info(f'Protein visualization result: {vis_result}')

        logger.info('All functionality tests completed successfully')
    except Exception as e:
        logger.error(f'An error occurred during functionality verification: {str(e)}', exc_info=True)

if __name__ == "__main__":
    verify_functionality()
