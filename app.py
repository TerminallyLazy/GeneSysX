import logging
import gradio as gr
import os
import tempfile
import traceback
from io import StringIO
from genesys.ai import run_conversation
from genesys.visuals import create_protein_interface
from genesys.client import upload_s3
from genesys import toolkit
from dotenv import load_dotenv
from flask import Flask, send_from_directory, request
import gradio.data_classes
import py3Dmol

# Configure static file serving
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
os.makedirs(static_dir, exist_ok=True)
print(f"Static directory absolute path: {static_dir}")

app = Flask(__name__, static_folder=static_dir, static_url_path='/static')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY"):
    logging.info("OpenAI API key is set")
else:
    logging.error("OpenAI API key is not set")

import base64

# Load custom CSS file
custom_css_path = os.path.join(static_dir, 'custom_style.css')
with open(custom_css_path, 'r') as css_file:
    custom_css = css_file.read()

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
    logger.info(f'Processing file input: {file_input}')
    if file_input is None:
        logger.warning("No file uploaded.")
        return "No file uploaded. Please upload a file."

    try:
        logger.info(f"File input type: {type(file_input)}")
        logger.info(f"File input attributes: {dir(file_input)}")

        file_content = None
        file_name = None

        # Handle different types of file inputs
        if isinstance(file_input, gr.File):
            file_name = file_input.name
            file_content = file_input.value
            logger.info(f"Input is a gr.File object: name={file_name}")
        elif isinstance(file_input, gradio.data_classes.FileData):
            file_name = file_input.name
            file_content = file_input.content
            logger.info(f"Input is a FileData object: name={file_name}")
        elif isinstance(file_input, dict):
            file_name = file_input.get('name', 'uploaded_file.txt')
            file_content = file_input.get('content', '')
            if not file_content:
                logger.error("Invalid dictionary input: missing 'content'")
                return "Invalid file input: missing required content"
            logger.info(f"Input is a dictionary: name={file_name}")
        elif isinstance(file_input, str):
            file_name = os.path.basename(file_input)
            try:
                with open(file_input, 'r') as f:
                    file_content = f.read()
            except IOError as e:
                logger.error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
            logger.info(f"Input is a string (file path): name={file_name}")
        elif isinstance(file_input, gradio.utils.NamedString):
            file_name = file_input.name
            file_content = str(file_input)
            logger.info(f"Input is a gradio.utils.NamedString object: name={file_name}, content length={len(file_content)}")
        elif hasattr(file_input, 'name') and hasattr(file_input, 'read'):
            file_name = file_input.name
            file_content = file_input.read()
            logger.info(f"Input is a file-like object: name={file_name}")
        else:
            logger.error(f"Unexpected file input type: {type(file_input)}")
            return f"Unexpected file input type: {type(file_input)}. Expected gr.File, FileData, dictionary with 'content', string file path, gradio.utils.NamedString, or file-like object."

        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')

        if file_content is None:
            logger.error("Unable to read file content")
            return "Unable to read file content. Please ensure you've uploaded a valid file and try again."

        logger.info(f"Processing file: {file_name}")
        logger.info(f"File content preview: {file_content[:100]}...")

        # Simplified file type detection
        file_type = 'FASTA' if file_content.strip().startswith('>') else os.path.splitext(file_name)[1][1:].upper()
        logger.info(f"File type detected: {file_type}")

        try:
            if file_type == 'FASTA':
                logger.info("Processing FASTA file")
                sequences = toolkit.parse_fasta(StringIO(file_content))
                num_sequences = len(sequences)
                total_length = sum(len(seq) for seq in sequences.values())
                avg_gc_content = sum(toolkit.gc_content(seq) for seq in sequences.values()) / num_sequences if num_sequences > 0 else 0
                sequence_type = toolkit.sequence_type(next(iter(sequences.values()))) if sequences else "Unknown"
                logger.info(f"FASTA processing complete: Sequences: {num_sequences}, Total Length: {total_length}, Avg GC Content: {avg_gc_content:.2f}%")
                result = f"File processed: {file_name}, Type: FASTA, Sequences: {num_sequences}, Total Length: {total_length}, Avg GC Content: {avg_gc_content:.2f}%, Sequence Type: {sequence_type}"
            elif file_type == 'PDB':
                logger.info(f"Processing PDB file: {file_name}")
                result = f"PDB file processed: {file_name}. Use Protein Visualization tab for further analysis."
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return f"Unsupported file type: {file_type}. Please upload a FASTA or PDB file."

            logger.info(f"File processing result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error processing file content {file_name}: {str(e)}", exc_info=True)
            return f"An error occurred while processing the file content {file_name}: {str(e)}"

    except Exception as e:
        logger.error(f'An error occurred in process_file: {str(e)}', exc_info=True)
        return f"An error occurred while processing the file: {str(e)}"

def answer_question(question, file):
    logger.info(f'Answering question: {question}')
    logger.info(f"File input: {file}")
    try:
        file_content = None
        file_name = None

        if isinstance(file, gr.File):
            logger.info(f"gr.File object attributes: {dir(file)}")
            file_name = getattr(file, 'name', 'uploaded_file.txt')
            if isinstance(file.value, dict):
                file_path = file.value.get('path')
                if file_path:
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                    except Exception as e:
                        logger.error(f"Error reading file from path: {str(e)}")
                else:
                    logger.error("File path not found in gr.File value dictionary")
            elif isinstance(file.value, str):
                try:
                    with open(file.value, 'r') as f:
                        file_content = f.read()
                except Exception as e:
                    logger.error(f"Error reading file from path: {str(e)}")
            elif hasattr(file, 'file'):
                try:
                    with open(file.file.name, 'r') as f:
                        file_content = f.read()
                except Exception as e:
                    logger.error(f"Error reading file.file: {str(e)}")

            if file_content is None:
                try:
                    file.seek(0)
                    file_content = file.read()
                except Exception as e:
                    logger.error(f"Error reading file as file-like object: {str(e)}")

            logger.info(f"File type: gr.File, File name: {file_name}")
            logger.info(f"File content type: {type(file_content)}")
        elif isinstance(file, gradio.data_classes.FileData):
            file_name = file.name
            file_content = file.content
            logger.info(f"File type: FileData, File name: {file_name}")
        elif isinstance(file, dict):
            file_name = file.get('name', 'uploaded_file.txt')
            file_content = file.get('content', '')
            if not file_content:
                logger.error("Invalid dictionary input: missing 'content'")
                return "Invalid file input: missing required content"
            logger.info(f"File type: dict, File name: {file_name}")
        elif isinstance(file, str):
            file_name = os.path.basename(file)
            try:
                with open(file, 'r') as f:
                    file_content = f.read()
            except IOError as e:
                logger.error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
            logger.info(f"File type: string (file path), File name: {file_name}")
        elif hasattr(file, 'name') and hasattr(file, 'read'):
            file_name = file.name
            file_content = file.read()
            logger.info(f"File type: file-like object, File name: {file_name}")
        else:
            logger.error(f"Unexpected file input type: {type(file)}")
            return f"Unexpected file input type: {type(file)}. Expected gr.File, FileData, dictionary with 'content', string file path, or file-like object."

        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')

        if file_content is None:
            logger.error("Unable to read file content")
            return "Unable to read file content. Please ensure you've uploaded a valid file and try again."

        logger.info(f"File content (first 100 chars): {file_content[:100] if file_content else 'Empty content'}")

        from genesys import toolkit

        def process_chunk(chunk):
            if "multiple sequence alignment" in question.lower():
                logger.info("Performing multiple sequence alignment")
                try:
                    from genesys.tools.sequence import multiple_sequence_alignment
                    alignment_result = multiple_sequence_alignment(StringIO(chunk))
                    logger.info(f"Alignment result (first 100 chars): {alignment_result[:100]}")
                    return f"Multiple sequence alignment result:\n\n{alignment_result}"
                except ImportError as ie:
                    logger.error(f"ImportError in multiple sequence alignment: {str(ie)}", exc_info=True)
                    return f"An error occurred while importing the multiple sequence alignment module: {str(ie)}"
                except Exception as e:
                    logger.error(f'An error occurred in multiple sequence alignment: {str(e)}', exc_info=True)
                    return f"An error occurred during multiple sequence alignment: {str(e)}"
            elif question.lower().strip() == "what are the sequence ids in the uploaded fasta file?":
                try:
                    sequence_ids = toolkit.extract_sequence_ids(StringIO(chunk))
                    return f"The sequence IDs in this chunk are: {', '.join(sequence_ids)}"
                except Exception as e:
                    logger.error(f'An error occurred while extracting sequence IDs: {str(e)}', exc_info=True)
                    return f"An error occurred while extracting sequence IDs: {str(e)}"
            else:
                try:
                    return run_conversation(question, StringIO(chunk))
                except Exception as e:
                    logger.error(f'An error occurred in run_conversation: {str(e)}', exc_info=True)
                    return f"An error occurred while processing your question: {str(e)}"

        chunk_size = 5000
        chunks = [file_content[i:i+chunk_size] for i in range(0, len(file_content), chunk_size)]
        logger.info(f"Processing file in {len(chunks)} chunks")

        answers = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            chunk_answer = process_chunk(chunk)
            answers.append(chunk_answer)

        answer = "\n".join(answers)
        logger.info(f"Answer received: {answer[:100]}...")  # Log first 100 characters of the answer
        logger.info("Returning answer from answer_question function")
        return answer
    except Exception as e:
        logger.error(f'An unexpected error occurred in answer_question: {str(e)}', exc_info=True)
        return f"An unexpected error occurred: {str(e)}. Please ensure you've uploaded a valid file and try again."

def create_interface():
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

            def process_file_wrapper(file):
                logger.info(f"File input in process_file_wrapper: {file}")
                logger.info(f"File input type in process_file_wrapper: {type(file)}")
                if file is None:
                    logger.warning("No file uploaded")
                    return "No file uploaded. Please upload a file.", ""
                try:
                    file_content = None
                    file_path = file.name if hasattr(file, 'name') else 'unknown'

                    if isinstance(file, gr.File):
                        logger.info(f"Input is gr.File: {file.name}")
                        file_path = file.name
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                    elif isinstance(file, gradio.data_classes.FileData):
                        logger.info(f"Input is FileData: {file.name}")
                        file_content = file.decode('utf-8')
                    else:
                        logger.error(f"Unexpected file input type: {type(file)}")
                        return f"Unexpected file input type: {type(file)}. Expected gr.File or FileData.", ""

                    if file_content is None:
                        logger.error("Failed to extract file content")
                        return "Failed to extract file content", ""

                    logger.info(f"Processing file: {file_path}")
                    logger.info(f"File content (first 100 chars): {file_content[:100]}")

                    file_info = f"{os.path.basename(file_path)} - {len(file_content)} characters"
                    try:
                        logger.info("Calling process_file function")
                        processed_content = process_file(file_content)
                        logger.info(f"File processing completed successfully. Result: {processed_content[:100]}...")
                        return processed_content, file_info
                    except Exception as e:
                        logger.error(f"Error in process_file: {str(e)}", exc_info=True)
                        return f"Error processing file: {str(e)}", file_info
                except Exception as e:
                    logger.error(f"Unexpected error in process_file_wrapper: {str(e)}", exc_info=True)
                    return f"Unexpected error processing file: {str(e)}", ""

            def answer_question_wrapper(question, file):
                logger.info(f"File input in answer_question_wrapper: {file}")
                logger.info(f"File input type in answer_question_wrapper: {type(file)}")
                logger.info(f"answer_question_wrapper received question: {question}")

                if file is None:
                    logger.warning("No file provided for question answering")
                    return "No file provided. Please upload a file before asking a question."

                try:
                    logger.info("Attempting to answer question")
                    answer = answer_question(question, file)
                    logger.info(f"Question answered successfully. Answer (first 100 chars): {answer[:100]}...")
                    return answer
                except Exception as e:
                    logger.error(f"Error in answer_question: {str(e)}", exc_info=True)
                    return f"Error answering question: {str(e)}"

            process_button.click(process_file_wrapper, inputs=[file_input], outputs=[output, file_info])
            answer_button.click(answer_question_wrapper, inputs=[question_input, file_input], outputs=[answer_output])
            download_button.click(lambda x: x, inputs=[file_input], outputs=[file_input])

        with gr.Tab("Protein Visualization"):
            pdb_file = gr.File(label="Upload PDB file")
            bg_color = gr.ColorPicker(label="Background Color", value="#FFFFFF")
            style = gr.Dropdown(["cartoon", "stick", "sphere", "surface"], label="Style", value="cartoon")
            spin = gr.Checkbox(label="Spin", value=True)
            visualize_button = gr.Button("Visualize Protein", elem_classes=["gradio-button"])
            viewer = gr.HTML(label="3D Viewer")

            def visualize_protein(file, bg_color, style, spin):
                if file is None:
                    return "Please upload a PDB file."

                try:
                    with open(file.name, 'r') as f:
                        pdb_content = f.read()

                    viewer = py3Dmol.view(width=600, height=400)
                    viewer.addModel(pdb_content, 'pdb')
                    viewer.setStyle({style: {'color': 'spectrum'}})
                    viewer.setBackgroundColor(bg_color)
                    if spin:
                        viewer.spin(True)
                    viewer.zoomTo()

                    return viewer.render()
                except Exception as e:
                    logger.error(f"Error in visualize_protein: {str(e)}", exc_info=True)
                    return f"Error visualizing protein: {str(e)}"

            visualize_button.click(
                visualize_protein,
                inputs=[pdb_file, bg_color, style, spin],
                outputs=[viewer]
            )

        # Expose API endpoints
        demo.load(fn=process_file, inputs=gr.File(), outputs=gr.Textbox(), api_name="process_file")
        demo.load(fn=answer_question, inputs=[gr.Textbox(), gr.File()], outputs=gr.Textbox(), api_name="answer_question")

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True, show_error=True)  # Enable public sharing and verbose error reporting
