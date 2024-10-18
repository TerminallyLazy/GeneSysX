import logging
import re

def add_logging_to_app():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    with open('app.py', 'r') as file:
        content = file.read()

    # Add import statement
    content = "import logging\n" + content

    # Add logger configuration
    content = content.replace("import gradio as gr", """import gradio as gr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
""")

    # Add logging to process_file function
    content = re.sub(
        r'def process_file\(file\):',
        '''def process_file(file):
    logger.info(f'Processing file: {file.name}')''',
        content
    )

    # Add logging to answer_question function
    content = re.sub(
        r'def answer_question\(question, file\):',
        '''def answer_question(question, file):
    logger.info(f'Answering question: {question}')''',
        content
    )

    # Add logging to visualize_protein function
    content = re.sub(
        r'def visualize_protein\(file, style, spin\):',
        '''def visualize_protein(file, style, spin):
    logger.info(f'Visualizing protein: {file.name}, Style: {style}, Spin: {spin}')''',
        content
    )

    # Add error logging
    content = content.replace('except Exception as e:', '''except Exception as e:
        logger.error(f'An error occurred: {str(e)}')''')

    with open('app.py', 'w') as file:
        file.write(content)

    logger.info('Logging statements added to app.py')

if __name__ == '__main__':
    add_logging_to_app()
