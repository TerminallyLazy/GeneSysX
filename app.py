import logging
import gradio as gr
import os
import tempfile
import traceback
import sys
from io import StringIO
from genesys.ai import run_conversation
from genesys.visuals import create_protein_interface, visualize_protein
from genesys.client import upload_s3
from genesys import toolkit
from dotenv import load_dotenv
from flask import Flask, send_from_directory, request
import gradio.data_classes
import py3Dmol

# Make visualize_protein function accessible for import

# Configure static file serving
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
os.makedirs(static_dir, exist_ok=True)
print(f"Static directory absolute path: {static_dir}")

app = Flask(__name__, static_folder=static_dir, static_url_path='/static')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("/tmp/genesysx_app.log", mode='a'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger(__name__)
logger.info("Logging initialized")
logger.debug("This is a test debug message")
logger.info("This is a test info message to verify logging is working")

# Force flush logs
for handler in logger.handlers:
    handler.flush()

@app.route('/static/<path:path>')
@app.route('/static/fonts/<path:path>')
def serve_static(path):
    full_path = os.path.join(static_dir, path)
    logger.info(f"Attempting to serve static file: {path}")
    logger.info(f"Full path: {full_path}")
    logger.info(f"File exists: {os.path.exists(full_path)}")
    logger.info(f"Static directory contents: {os.listdir(static_dir)}")
    logger.info(f"Request headers: {request.headers}")
    try:
        if os.path.exists(full_path):
            return send_from_directory(static_dir, path)
        else:
            logger.error(f"File not found: {full_path}")
            return f"Error: File not found {path}", 404
    except Exception as e:
        logger.error(f"Failed to serve static file: {path}. Error: {str(e)}")
        logger.error(f"Full error traceback: {traceback.format_exc()}")
        return f"Error: Could not serve file {path}", 500

# Check if font files exist
font_files = ['ui-sans-serif-Regular.woff2', 'ui-sans-serif-Bold.woff2', 'system-ui-Regular.woff2', 'system-ui-Bold.woff2']

load_dotenv()

# Check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY"):
    logging.info("OpenAI API key is set")
else:
    logging.error("OpenAI API key is not set")

import base64

# Load custom CSS file
custom_css_path = os.path.join(static_dir, 'custom_style.css')
with open(custom_css_path, 'r') as f:
    custom_css = f.read()

# CSS string with @font-face rules and custom CSS
css = f"""
@font-face {{
    font-family: 'UI Sans Serif';
    src: url('/static/ui-sans-serif-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
@font-face {{
    font-family: 'UI Sans Serif';
    src: url('/static/ui-sans-serif-Bold.woff2') format('woff2');
    font-weight: bold;
    font-style: normal;
}}
@font-face {{
    font-family: 'System UI';
    src: url('/static/system-ui-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}}
@font-face {{
    font-family: 'System UI';
    src: url('/static/system-ui-Bold.woff2') format('woff2');
    font-weight: bold;
    font-style: normal;
}}
{custom_css}
"""

# Ensure static files are present
font_files = ['ui-sans-serif-Regular.woff2', 'ui-sans-serif-Bold.woff2', 'system-ui-Regular.woff2', 'system-ui-Bold.woff2']
for font_file in font_files:
    font_path = os.path.join(static_dir, font_file)
    if not os.path.exists(font_path):
        logger.warning(f"Font file not found: {font_path}")
    else:
        logger.info(f"Font file present: {font_path}")

def process_file(file_input):
    logger.info("==== START OF PROCESS_FILE FUNCTION ====")
    logger.info(f'Processing file input: {file_input}')
    logger.info(f'File input type: {type(file_input)}')
    logger.info(f'Current working directory: {os.getcwd()}')
    logger.info(f'Exact content of file_input:\n{file_input}')
    if file_input is None:
        logger.warning("No file uploaded.")
        return {"status": "error", "message": "No file uploaded. Please upload a file."}
    try:
        logger.info(f"File input type: {type(file_input)}")
        logger.info(f"File input attributes: {dir(file_input)}")

        file_content = None
        file_name = None
        file_path = None

        # Handle different types of file inputs
        if isinstance(file_input, gr.File):
            file_name = file_input.name
            file_content = file_input.value
            file_path = file_input.name
            logger.info(f"Input is a gr.File object: name={file_name}, path={file_path}")
        elif isinstance(file_input, gradio.data_classes.FileData):
            file_name = file_input.name
            file_content = file_input.content
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
                temp_file.write(file_content)
                file_path = temp_file.name
            logger.info(f"Input is a FileData object: name={file_name}, path={file_path}")
        elif isinstance(file_input, dict):
            file_name = file_input.get('name', 'uploaded_file.txt')
            file_content = file_input.get('content', '')
            file_path = file_input.get('path')
            if not file_content and not file_path:
                logger.error("Invalid dictionary input: missing 'content' and 'path'")
                return {"status": "error", "message": "Invalid file input: missing required content or path"}
            if not file_path:
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
                    temp_file.write(file_content)
                    file_path = temp_file.name
            elif not file_content:
                try:
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                except IOError as e:
                    logger.error(f"Error reading file: {str(e)}")
                    return {"status": "error", "message": f"Error reading file: {str(e)}", "file_path": file_path}
            logger.info(f"Input is a dictionary: name={file_name}, path={file_path}")
        elif isinstance(file_input, str):
            file_name = os.path.basename(file_input)
            file_path = file_input
            try:
                with open(file_input, 'r') as f:
                    file_content = f.read()
            except IOError as e:
                logger.error(f"Error reading file: {str(e)}")
                return {"status": "error", "message": f"Error reading file: {str(e)}", "file_path": file_path}
            logger.info(f"Input is a string (file path): name={file_name}, path={file_path}")
        elif isinstance(file_input, gradio.utils.NamedString):
            file_name = file_input.name
            file_content = str(file_input)
            file_path = file_name  # Use the name as the path since we're not creating a temporary file
            logger.info(f"Input is a gradio.utils.NamedString object: name={file_name}")
        else:
            error_msg = f"Unexpected file input type: {type(file_input)}. Expected gr.File, FileData, dictionary with 'content' or 'path', string file path, or NamedString-like object."
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        if isinstance(file_content, bytes):
            try:
                file_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                logger.error("Failed to decode file content as UTF-8")
                return {"status": "error", "message": "Failed to decode file content. Please ensure the file is in a valid text format.", "file_path": file_path}

        if file_content is None:
            logger.error("Unable to read file content")
            return {"status": "error", "message": "Unable to read file content. Please ensure you've uploaded a valid file and try again.", "file_path": file_path}

        logger.info(f"Processing file: {file_name}")
        logger.info(f"File content (first 100 characters): {file_content[:100]}")
        logger.info(f"Full file content:\n{file_content}")

        # File type detection
        file_extension = os.path.splitext(file_name)[1].lower()
        file_content_stripped = file_content.strip()

        logger.info(f"File extension: {file_extension}")
        logger.info(f"First line of file content: {file_content_stripped.split('\n')[0]}")

        def is_fasta_file(file_content, file_name):
            fasta_extensions = ['.fasta', '.fa', '.fna', '.ffn', '.faa', '.frn']
            file_extension = os.path.splitext(file_name)[1].lower()
            has_fasta_header = any(line.strip().startswith('>') for line in file_content.split('\n') if line.strip())
            is_fasta = file_extension in fasta_extensions or has_fasta_header
            logger.info(f"FASTA detection: extension={file_extension}, has_header={has_fasta_header}, is_fasta={is_fasta}")
            return is_fasta

        def is_csv_file(file_content, file_name):
            file_extension = os.path.splitext(file_name)[1].lower()
            first_line = file_content.strip().split('\n')[0]
            is_csv = file_extension == '.csv' or ',' in first_line
            logger.info(f"CSV detection: extension={file_extension}, has_comma={(',' in first_line)}, is_csv={is_csv}")
            return is_csv

        def is_pdb_file(file_content, file_name):
            file_extension = os.path.splitext(file_name)[1].lower()
            first_line = file_content.strip().split('\n')[0]
            is_pdb = file_extension == '.pdb' or first_line.startswith(('HEADER', 'ATOM'))
            logger.info(f"PDB detection: extension={file_extension}, starts_with_header_or_atom={first_line.startswith(('HEADER', 'ATOM'))}, is_pdb={is_pdb}")
            return is_pdb

        def process_fasta(content):
            logger.info("Processing FASTA file")
            try:
                lines = content.strip().split('\n')
                sequence_ids = [line[1:].split()[0] for line in lines if line.startswith('>')]
                num_sequences = len(sequence_ids)
                logger.info(f"Extracted {num_sequences} sequence IDs from FASTA file")
                sample_ids = sequence_ids[:10] if num_sequences > 10 else sequence_ids
                result = {
                    "status": "success",
                    "message": f"Successfully processed FASTA file with {num_sequences} sequences",
                    "num_sequences": num_sequences,
                    "sequence_ids_sample": sample_ids
                }
                logger.info(f"FASTA processing result: {result}")
                return result
            except Exception as e:
                logger.error(f"Error processing FASTA file: {str(e)}", exc_info=True)
                return {"status": "error", "message": f"Error processing FASTA file: {str(e)}"}

        def process_csv(content):
            logger.info("Processing CSV file")
            try:
                lines = content.strip().split('\n')
                num_rows = len(lines)
                num_columns = len(lines[0].split(',')) if num_rows > 0 else 0
                logger.info(f"CSV processing complete. Number of rows: {num_rows}, Number of columns: {num_columns}")
                result = {"status": "success", "num_rows": num_rows, "num_columns": num_columns}
                logger.info(f"CSV processing result: {result}")
                return result
            except Exception as e:
                logger.error(f"Error processing CSV file: {str(e)}", exc_info=True)
                return {"status": "error", "message": f"Error processing CSV file: {str(e)}"}

        def process_pdb(content):
            logger.info("Processing PDB file")
            try:
                lines = content.split('\n')
                num_atoms = sum(1 for line in lines if line.startswith('ATOM'))
                num_hetatm = sum(1 for line in lines if line.startswith('HETATM'))
                logger.info(f"PDB processing complete. Number of atoms: {num_atoms}, Number of HETATM: {num_hetatm}")
                result = {"status": "success", "num_atoms": num_atoms, "num_hetatm": num_hetatm}
                logger.info(f"PDB processing result: {result}")
                return result
            except Exception as e:
                logger.error(f"Error processing PDB file: {str(e)}", exc_info=True)
                return {"status": "error", "message": f"Error processing PDB file: {str(e)}"}

        # Detect file type and process accordingly
        if is_fasta_file(file_content, file_name):
            file_type = 'FASTA'
            process_func = process_fasta
        elif is_csv_file(file_content, file_name):
            file_type = 'CSV'
            process_func = process_csv
        elif is_pdb_file(file_content, file_name):
            file_type = 'PDB'
            process_func = process_pdb
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return {"status": "error", "message": f"Unsupported file type: {file_extension}. Please upload a FASTA, CSV, or PDB file."}

        logger.info(f"Detected file type: {file_type}")

        # Process file based on type
        try:
            processed_data = process_func(file_content)
            if processed_data["status"] == "success":
                return {
                    "status": "success",
                    "message": f"Successfully processed {file_type} file.",
                    "file_type": file_type,
                    "processed_data": processed_data,
                    "file_content": file_content,
                    "file_path": file_path
                }
            else:
                return processed_data
        except Exception as e:
            logger.error(f"An error occurred while processing the {file_type} file: {str(e)}", exc_info=True)
            return {"status": "error", "message": f"An error occurred while processing the {file_type} file: {str(e)}", "file_path": file_path}

    except Exception as e:
        logger.error(f'An error occurred in process_file: {str(e)}', exc_info=True)
        return {"status": "error", "message": f"An error occurred while processing the file: {str(e)}", "file_path": file_path}

def answer_question(question, file):
    logger.info(f'Answering question: {question}')
    logger.info(f"File input type: {type(file)}")
    logger.info(f"File input details: {file}")
    try:
        # Use process_file to handle file input and get processed content
        logger.info("Attempting to process file")
        logger.debug(f"Raw file content (first 200 chars): {file['content'][:200] if isinstance(file, dict) and 'content' in file else str(file)[:200]}")
        processed_result = process_file(file)
        logger.debug(f"Processed result: {processed_result}")
        if processed_result['status'] == 'error':
            logger.error(f"Error in process_file: {processed_result['message']}")
            return processed_result['message']

        file_content = processed_result.get('file_content', '')
        if not file_content:
            logger.error("No file content found in processed result")
            return "Error: No file content found. Please try uploading the file again."

        logger.info(f"Processed file content type: {type(file_content)}")
        logger.info(f"Processed file content length: {len(file_content)}")
        logger.info(f"Processed file content preview (first 200 chars): {file_content[:200]}")

        try:
            # Limit file content to prevent exceeding token limits
            max_content_length = 4000  # Adjust this value based on your token limit
            truncated_content = file_content[:max_content_length]
            file_content_io = StringIO(truncated_content)
            file_content_io.seek(0)

            logger.debug("Preparing to call run_conversation function")
            logger.debug(f"Question being passed to run_conversation: {question}")
            logger.debug(f"File content type being passed to run_conversation: {type(file_content_io)}")
            logger.debug(f"File content preview being passed to run_conversation (first 200 chars): {file_content_io.getvalue()[:200]}")
            logger.debug(f"Full file content being passed to run_conversation: {file_content_io.getvalue()}")

            logger.debug("Calling run_conversation function")
            try:
                conversation_result = run_conversation(question, file_content_io)
                logger.debug("run_conversation function call completed")
                logger.debug(f"Raw conversation result type: {type(conversation_result)}")
                logger.debug(f"Raw conversation result: {conversation_result}")
            except Exception as e:
                logger.error(f"Error in run_conversation: {str(e)}", exc_info=True)
                return f"An error occurred while processing your question: {str(e)}. Please try again."

            logger.debug(f"Conversation result: {conversation_result}")
            if conversation_result is None:
                logger.error("Conversation result is None")
                return "Failed to generate an answer. Please try again."
            elif isinstance(conversation_result, dict):
                if 'answer' in conversation_result:
                    answer = conversation_result['answer']
                    logger.info(f"Generated answer preview (first 200 chars): {answer[:200]}")
                    return answer
                else:
                    logger.error("Conversation result is a dictionary but does not contain 'answer' key")
                    logger.error(f"Conversation result keys: {conversation_result.keys()}")
                    return "Received an unexpected answer format. Please try again."
            elif isinstance(conversation_result, str):
                if not conversation_result.strip():
                    logger.error("Conversation result is empty or whitespace")
                    return "Generated answer is empty. Please try rephrasing your question."
                logger.info(f"Generated answer preview (first 200 chars): {conversation_result[:200]}")
                return conversation_result
            else:
                logger.error(f"Unexpected conversation result type: {type(conversation_result)}")
                logger.error(f"Unexpected conversation result content: {conversation_result}")
                return "Received an unexpected answer format. Please try again."

        except IndexError as e:
            logger.error(f'Slicing error in run_conversation: {str(e)}', exc_info=True)
            return f"An error occurred while processing the answer: {str(e)}. This might be due to an empty or invalid response."
        except ValueError as e:
            logger.error(f'Value error in run_conversation: {str(e)}', exc_info=True)
            return f"An error occurred while processing the input: {str(e)}. Please check your input and try again."
        except AttributeError as e:
            logger.error(f'Attribute error in run_conversation: {str(e)}', exc_info=True)
            return f"An error occurred while accessing data: {str(e)}. Please ensure the file content is in the correct format."
        except Exception as e:
            logger.error(f'Error generating answer: {str(e)}', exc_info=True)
            return f"An error occurred while generating the answer: {str(e)}. Please try rephrasing your question or uploading a different file."
    except Exception as e:
        logger.error(f'Unexpected error in answer_question: {str(e)}', exc_info=True)
        return f"An unexpected error occurred: {str(e)}. Please ensure you've uploaded a valid file and try again."

def create_interface():
    logger.info("Starting create_interface function")
    with open('custom_style.css', 'r') as f:
        custom_css = f.read()

    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("# 🧬 GeneSysX Gradio App")

        with gr.Accordion("Quick Start Guide", open=False):
            gr.Markdown("## Installation")
            gr.Markdown("1. 📥 Clone the repo: `git clone https://github.com/TerminallyLazy/GeneSys-X.git`")
            gr.Markdown("2. 📦 Install dependencies: `pip install -r requirements.txt`")
            gr.Markdown("3. 🚀 Run the app: `python app.py`")
            gr.Markdown("## Usage")
            gr.Markdown("1. 📤 Upload a file (FASTA, CSV, or PDB)")
            gr.Markdown("2. 🔍 Click 'Process File' to analyze")
            gr.Markdown("3. ❓ Ask a question about the data")
            gr.Markdown("4. 🧬 For PDB files, check the Protein Visualization tab")
            gr.Markdown("Example: Upload a FASTA file, process it, then ask 'What are the sequence IDs in the uploaded FASTA file?'")

        with gr.Tab("File Processing"):
            with gr.Row(elem_classes=["container"]):
                file_input = gr.File(label="Upload File (FASTA, CSV, or PDB)")
                file_info = gr.Markdown(elem_classes=["file-info"])
                download_button = gr.Button("⬇️", elem_classes=["download-button"])

            with gr.Column(elem_classes=["container"]):
                process_button = gr.Button("Process File", elem_classes=["gradio-button"])
                output = gr.Textbox(label="Processing Result", lines=5, elem_classes=["gradio-output"])

            with gr.Column(elem_classes=["container"]):
                with gr.Row():
                    question_input = gr.Textbox(label="Ask a question about the data", placeholder="Tell me ID", lines=1, elem_classes=["gradio-input"])
                    answer_button = gr.Button("Get Answer", elem_classes=["gradio-button"])
                answer_output = gr.Textbox(label="Answer", lines=10, elem_classes=["gradio-output"])

        with gr.Tab("Protein Visualization"):
            pdb_file = gr.File(label="Upload PDB file")
            bg_color = gr.ColorPicker(label="Background Color", value="#FFFFFF")
            style = gr.Dropdown(["cartoon", "stick", "sphere", "surface"], label="Style", value="cartoon")
            spin = gr.Checkbox(label="Spin", value=True)
            visualize_button = gr.Button("Visualize Protein", elem_classes=["gradio-button"])
            viewer = gr.HTML(label="3D Viewer")

        def process_file_wrapper(file):
            from io import StringIO
            import sys

            # Capture logs
            log_capture = StringIO()
            log_handler = logging.StreamHandler(log_capture)
            logger.addHandler(log_handler)

            logger.info(f"File input in process_file_wrapper: {file}")
            logger.info(f"File input type in process_file_wrapper: {type(file)}")
            logger.info(f"File attributes: {dir(file)}")
            logger.info(f"File repr: {repr(file)}")
            if file is None:
                logger.warning("No file uploaded")
                return "No file uploaded. Please upload a file.", "", log_capture.getvalue()
            try:
                file_input = {}
                if isinstance(file, gradio.data_classes.FileData):
                    logger.info("File input is gradio.data_classes.FileData")
                    file_input = {"name": file.name, "path": file.path}
                    logger.info(f"FileData name: {file.name}, path: {file.path}")
                    with open(file.path, 'r', encoding='utf-8') as f:
                        file_input["content"] = f.read()
                    logger.info(f"FileData content preview: {file_input['content'][:100]}")
                elif isinstance(file, gradio.utils.NamedString):
                    logger.info("File input is gradio.utils.NamedString")
                    file_input = {"name": file.name, "content": str(file)}
                    logger.info(f"NamedString name: {file.name}, content preview: {file_input['content'][:100]}")
                elif isinstance(file, dict):
                    logger.info("File input is a dictionary")
                    file_input = file
                    logger.info(f"Dictionary keys: {file.keys()}")
                    if 'path' in file and 'content' not in file:
                        with open(file['path'], 'r', encoding='utf-8') as f:
                            file_input["content"] = f.read()
                    logger.info(f"Dictionary content preview: {file_input.get('content', '')[:100]}")
                elif isinstance(file, str):
                    logger.info("File input is a string (likely a file path)")
                    file_input = {"name": os.path.basename(file), "path": file}
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            file_input["content"] = f.read()
                        logger.info(f"File content preview: {file_input['content'][:100]}")
                    except Exception as e:
                        logger.error(f"Error reading file content: {str(e)}")
                        return f"Error: Unable to read file content: {str(e)}", "", log_capture.getvalue()
                else:
                    logger.error(f"Unexpected file input type: {type(file)}")
                    return f"Error: Unexpected file input type: {type(file)}. Expected FileData, NamedString, dict, or str.", "", log_capture.getvalue()

                if 'content' not in file_input:
                    logger.error("File input missing content")
                    return "Error: Unable to read file content.", "", log_capture.getvalue()

                logger.info(f"Processing file: {file_input.get('name', 'Unknown')}")
                logger.info(f"File content preview (first 100 chars): {file_input['content'][:100]}")
                logger.info(f"File size: {len(file_input['content'])} bytes")

                file_info = f"{file_input.get('name', 'Unknown')} - {len(file_input['content'])} characters"
                try:
                    logger.info("Calling process_file function")
                    processed_content = process_file(file_input)
                    logger.info(f"File processing completed. Result type: {type(processed_content)}")
                    if isinstance(processed_content, dict):
                        logger.info(f"Processing result: {processed_content}")
                        return f"File processed successfully. {processed_content.get('message', 'Unknown result')}", file_info, log_capture.getvalue()
                    else:
                        logger.info(f"File processing completed successfully. Result preview: {str(processed_content)[:100]}...")
                        return f"File processed successfully. Type: {type(processed_content).__name__}", file_info, log_capture.getvalue()
                except Exception as e:
                    logger.error(f"Error in process_file: {str(e)}", exc_info=True)
                    return f"Error processing file: {str(e)}", file_info, log_capture.getvalue()
            except Exception as e:
                logger.error(f"Unexpected error in process_file_wrapper: {str(e)}", exc_info=True)
                return f"Error: Unexpected error processing file: {str(e)}", "", log_capture.getvalue()
            finally:
                logger.removeHandler(log_handler)

        def visualize_protein_wrapper(pdb_file, bg_color, style, spin):
            try:
                logger.info(f"Visualizing protein: {pdb_file}")
                logger.info(f"Input parameters: bg_color={bg_color}, style={style}, spin={spin}")
                if isinstance(pdb_file, gradio.data_classes.FileData):
                    pdb_content = pdb_file.data
                    original_file_name = pdb_file.name
                    logger.info(f"FileData input: name={original_file_name}, content length={len(pdb_content)}")
                elif isinstance(pdb_file, gr.File):
                    with open(pdb_file.name, 'r', encoding='utf-8') as f:
                        pdb_content = f.read()
                    original_file_name = pdb_file.name
                    logger.info(f"gr.File input: name={original_file_name}, content length={len(pdb_content)}")
                elif isinstance(pdb_file, dict):
                    pdb_content = pdb_file.get('content', '')
                    original_file_name = pdb_file.get('name', 'unknown')
                    logger.info(f"Dict input: name={original_file_name}, content length={len(pdb_content)}")
                elif isinstance(pdb_file, str):
                    if os.path.isfile(pdb_file):
                        with open(pdb_file, 'r', encoding='utf-8') as f:
                            pdb_content = f.read()
                        original_file_name = os.path.basename(pdb_file)
                        logger.info(f"Local file input: name={original_file_name}, content length={len(pdb_content)}")
                    else:
                        logger.error(f"Invalid PDB file path: {pdb_file}")
                        return {"status": "error", "message": "Error: Invalid PDB file path"}
                else:
                    logger.error(f"Unexpected PDB file input type: {type(pdb_file)}")
                    return {"status": "error", "message": "Error: Invalid PDB file input"}

                import tempfile
                file_extension = os.path.splitext(original_file_name)[1] or '.pdb'
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(pdb_content)
                    pdb_path = temp_file.name
                logger.info(f"Created temporary PDB file: {pdb_path}")

                visualization_result = visualize_protein(pdb_path, bg_color, style, spin)
                logger.info(f"Visualization result: {visualization_result}")
                return visualization_result
            except Exception as e:
                logger.error(f"Error in visualize_protein_wrapper: {str(e)}", exc_info=True)
                return {"status": "error", "message": f"Error visualizing protein: {str(e)}"}

        def answer_question_wrapper(question, file):
            logger.info(f"File input in answer_question_wrapper: {file}")
            logger.info(f"File input type in answer_question_wrapper: {type(file)}")
            logger.info(f"answer_question_wrapper received question: {question}")

            if file is None:
                logger.warning("No file provided for question answering")
                return "No file provided. Please upload a file before asking a question."

            try:
                if isinstance(file, gradio.data_classes.FileData):
                    file_input = {"name": file.name, "content": file.content}
                elif isinstance(file, gr.File):
                    with open(file.name, 'r', encoding='utf-8') as f:
                        file_input = {"name": file.name, "content": f.read()}
                elif isinstance(file, dict):
                    file_input = file
                elif isinstance(file, gradio.utils.NamedString):
                    file_input = {"name": file.name, "content": str(file)}
                elif isinstance(file, str):
                    with open(file, 'r', encoding='utf-8') as f:
                        file_input = {"name": os.path.basename(file), "content": f.read()}
                else:
                    error_msg = f"Unexpected file input type: {type(file)}. Expected FileData, gr.File, dict, NamedString, or file path string."
                    logger.error(error_msg)
                    return error_msg

                logger.info(f"Processing file: {file_input['name']}")
                logger.info(f"File content (first 100 characters): {file_input['content'][:100]}")

                logger.info("Attempting to answer question")
                answer = answer_question(question, file_input)

                if not isinstance(answer, str):
                    error_msg = f"Unexpected answer type: {type(answer)}. Expected string."
                    logger.error(error_msg)
                    return error_msg

                logger.info(f"Question answered successfully. Answer (first 100 chars): {answer[:100]}...")
                return answer
            except Exception as e:
                error_msg = f"Error answering question: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"An error occurred while processing your question: {error_msg}. Please try again or contact support if the issue persists."

def visualize_protein(file, bg_color, style, spin):
    """
    Visualize a protein structure from a PDB file or PDB ID.

    Args:
        file (str or FileUpload): PDB file path, PDB ID, or uploaded file object
        bg_color (str): Background color for the visualization
        style (str): Visualization style (e.g., 'cartoon', 'stick')
        spin (bool): Whether to enable spinning of the protein structure

    Returns:
        dict: A dictionary containing the status and either the HTML content of the visualization or an error message
    """
    logger.info(f"Starting visualize_protein function. File: {file}, Background color: {bg_color}, Style: {style}, Spin: {spin}")
    if file is None or (isinstance(file, str) and file.strip() == ""):
        logger.warning("No file uploaded or invalid input for protein visualization")
        return {"status": "error", "message": "Please upload a PDB file or provide a valid PDB ID."}

    if bg_color not in ["white", "black", "grey"]:
        logger.warning(f"Invalid background color: {bg_color}")
        return {"status": "error", "message": "Invalid background color. Please choose white, black, or grey."}

    if style not in ["cartoon", "stick", "sphere"]:
        logger.warning(f"Invalid style: {style}")
        return {"status": "error", "message": "Invalid style. Please choose cartoon, stick, or sphere."}

    try:
        if isinstance(file, str):  # Assume it's a PDB ID
            logger.info(f"Detected PDB ID: {file}. Attempting to download PDB file.")
            try:
                import urllib.request
                url = f"https://files.rcsb.org/download/{file}.pdb"
                with urllib.request.urlopen(url) as response:
                    pdb_content = response.read().decode('utf-8')
                logger.info(f"Successfully downloaded PDB file for ID: {file}. Content length: {len(pdb_content)}")
            except urllib.error.URLError as e:
                logger.error(f"Failed to download PDB file for ID {file}: {str(e)}")
                return {"status": "error", "message": f"Failed to download PDB file: {str(e)}"}
        else:  # Assume it's a file upload
            logger.info(f"Detected file upload. Attempting to read uploaded PDB file: {file.name}")
            try:
                with open(file.name, 'r') as f:
                    pdb_content = f.read()
                logger.info(f"Successfully read PDB file: {file.name}. Content length: {len(pdb_content)}")
            except IOError as e:
                logger.error(f"Failed to read uploaded PDB file {file.name}: {str(e)}")
                return {"status": "error", "message": f"Failed to read uploaded file: {str(e)}"}

        logger.info("Initializing py3Dmol viewer")
        viewer = py3Dmol.view(width=600, height=400)
        logger.info("Adding model to py3Dmol viewer")
        viewer.addModel(pdb_content, 'pdb')
        logger.info(f"Setting style: {style}")
        viewer.setStyle({style: {'color': 'spectrum'}})
        logger.info(f"Setting background color: {bg_color}")
        viewer.setBackgroundColor(bg_color)
        if spin:
            logger.info("Enabling spin")
            viewer.spin(True)
        viewer.zoomTo()

        logger.info("Rendering protein visualization")
        rendered_view = viewer.render()
        logger.info(f"Protein visualization rendered successfully. HTML content length: {len(rendered_view)}")
        visualization_result = create_protein_interface(rendered_view, bg_color, style, spin)
        logger.info(f"Visualization interface created. Result length: {len(visualization_result)}")
        return {"status": "success", "visualization": visualization_result}
    except Exception as e:
        logger.error(f"Unexpected error in visualize_protein: {str(e)}", exc_info=True)
        return {"status": "error", "message": f"An unexpected error occurred while visualizing the protein: {str(e)}"}

def create_interface():
    def process_file_wrapper(file):
        result = process_file(file)
        return result.get('message', ''), result.get('file_info', '')

    def answer_question_wrapper(question, file):
        result = answer_question(question, file)
        return result

    def visualize_protein_wrapper(file, bg_color, style, spin):
        result = visualize_protein(file, bg_color, style, spin)
        return result.get('visualization', '')

    with gr.Blocks(css=css) as demo:
        gr.Markdown("# GeneSysX: Genomic Data Analysis")

        with gr.Tab("File Processing"):
            file_input = gr.File(label="Upload File")
            process_button = gr.Button("Process File")
            output = gr.Textbox(label="Processing Output")
            file_info = gr.Markdown(label="File Information")

        with gr.Tab("Q&A"):
            question_input = gr.Textbox(label="Enter your question")
            answer_button = gr.Button("Get Answer")
            answer_output = gr.Textbox(label="Answer")

        with gr.Tab("Protein Visualization"):
            pdb_file = gr.File(label="Upload PDB File")
            bg_color = gr.Dropdown(["white", "black", "grey"], label="Background Color")
            style = gr.Dropdown(["cartoon", "stick", "sphere"], label="Visualization Style")
            spin = gr.Checkbox(label="Enable Spin")
            visualize_button = gr.Button("Visualize Protein")
            viewer = gr.HTML(label="Protein Viewer")

        process_button.click(process_file_wrapper, inputs=[file_input], outputs=[output, file_info])
        answer_button.click(answer_question_wrapper, inputs=[question_input, file_input], outputs=[answer_output])
        visualize_button.click(
            visualize_protein_wrapper,
            inputs=[pdb_file, bg_color, style, spin],
            outputs=[viewer]
        )

        # Expose API endpoints
        demo.load(fn=process_file_wrapper, inputs=gr.File(), outputs=[gr.Textbox(), gr.Markdown()], api_name="process_file_wrapper")
        demo.load(fn=answer_question_wrapper, inputs=[gr.Textbox(), gr.File()], outputs=gr.Textbox(), api_name="answer_question_wrapper")
        demo.load(fn=visualize_protein_wrapper, inputs=[gr.File(), gr.Dropdown(), gr.Dropdown(), gr.Checkbox()], outputs=gr.HTML(), api_name="visualize_protein_wrapper")

    logger.info("Interface created successfully. Preparing to launch...")
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True, show_error=True)  # Enable public sharing and verbose error reporting
