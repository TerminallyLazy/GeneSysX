import gradio as gr
import os
import logging
import tempfile
from io import StringIO
from genesys.ai import run_conversation
from genesys.visuals import create_protein_interface
from genesys.client import upload_s3
from genesys import toolkit
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY"):
    logging.info("OpenAI API key is set")
else:
    logging.error("OpenAI API key is not set")

def process_file(file):
    if file is None:
        return "No file uploaded. Please upload a file."

    try:
        if isinstance(file, dict):
            file_obj = file['file']
            file_name = file['name']
        elif isinstance(file, str):
            file_obj = file
            file_name = os.path.basename(file)
        else:
            file_obj = file.file if hasattr(file, 'file') else file
            file_name = file.name if hasattr(file, 'name') else os.path.basename(file_obj.name)

        file_type = os.path.splitext(file_name)[1][1:].upper()

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type.lower()}') as temp_file:
            if isinstance(file_obj, str):
                with open(file_obj, 'rb') as f:
                    file_content = f.read()
            elif isinstance(file_obj, bytes):
                file_content = file_obj
            else:
                file_content = file_obj.read()

            temp_file.write(file_content)
            temp_file_path = temp_file.name

        if file_type == 'FASTA':
            sequence_type = toolkit.sequence_type(temp_file_path)
            gc_content = toolkit.gc_content(temp_file_path)
            logging.info(f"Processing FASTA file: {file_name}")
            result = f"File processed: {file_name}, Type: {file_type}, Sequence Type: {sequence_type}, GC Content: {gc_content:.2f}%"
        elif file_type == 'PDB':
            logging.info(f"Processing PDB file: {file_name}")
            result = f"PDB file processed: {file_name}. Use Protein Visualization tab for further analysis."
        else:
            logging.info(f"Processing file: {file_name}")
            result = f"File processed: {file_name}, Type: {file_type}"

        os.unlink(temp_file_path)
        return result
    except Exception as e:
        logging.error(f"Error in process_file: {str(e)}", exc_info=True)
        return f"An error occurred while processing the file: {str(e)}"

def answer_question(question, file):
    logging.debug(f"Answering question: '{question}' for file: {file}")
    try:
        if isinstance(file, dict):
            file_path = file['name']
            file_content = file['file'].read().decode('utf-8')
            logging.debug(f"File type: dict, File path: {file_path}")
        elif isinstance(file, str):
            file_path = file
            with open(file_path, 'r') as f:
                file_content = f.read()
            logging.debug(f"File type: str, File path: {file_path}")
        else:
            file_path = file.name
            file_content = file.read().decode('utf-8')
            logging.debug(f"File type: other, File path: {file_path}")

        logging.debug(f"File content (first 100 chars): {file_content[:100]}")

        if "multiple sequence alignment" in question.lower():
            from genesys.sequence import multiple_sequence_alignment
            alignment_result = multiple_sequence_alignment(file_path)
            answer = f"Multiple sequence alignment result:\n\n{alignment_result}"
        elif question.lower().strip() == "what are the sequence ids in the uploaded fasta file?":
            sequence_ids = toolkit.extract_sequence_ids(file_content)
            answer = f"The sequence IDs in the uploaded FASTA file are: {', '.join(sequence_ids)}"
        else:
            answer = run_conversation(question, file_path)

        logging.debug(f"Answer received: {answer[:100]}...")  # Log first 100 characters of the answer
        logging.debug("Returning answer from answer_question function")
        return answer
    except Exception as e:
        logging.error(f"Error in answer_question: {str(e)}", exc_info=True)
        return f"An error occurred: {str(e)}. Please ensure you've uploaded a valid FASTA file."

def create_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🧬 GeneSysX Gradio App")

        with gr.Row():
            theme_dropdown = gr.Dropdown(choices=["light", "dark"], label="Theme", value="light")
            font_size_slider = gr.Slider(minimum=12, maximum=24, value=16, step=1, label="Font Size")

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
            with gr.Row():
                file_input = gr.File(label="Upload File (FASTA, CSV, or PDB)")
                process_button = gr.Button("Process File", variant="primary")
                clear_file_button = gr.Button("Clear File")
            output = gr.Textbox(label="Processing Result", lines=5)

            with gr.Row():
                question_input = gr.Textbox(label="Ask a question about the data", lines=2)
                answer_button = gr.Button("Get Answer", variant="primary")
                clear_question_button = gr.Button("Clear Question")
            answer_output = gr.Textbox(label="Answer", lines=10)

            process_button.click(process_file, inputs=[file_input], outputs=[output])
            answer_button.click(answer_question, inputs=[question_input, file_input], outputs=[answer_output])
            clear_file_button.click(lambda: None, inputs=[], outputs=[file_input])
            clear_question_button.click(lambda: "", inputs=[], outputs=[question_input])

        with gr.Tab("Protein Visualization"):
            try:
                logging.info("Initializing Protein Visualization interface")
                protein_interface = create_protein_interface()
                logging.info("Protein Visualization interface initialized successfully")
            except Exception as e:
                logging.error(f"Error initializing Protein Visualization interface: {str(e)}")
                gr.Markdown("An error occurred while loading the Protein Visualization interface. Please check the logs for more information.")

        def update_theme(theme):
            if theme == "dark":
                return gr.themes.Default()
            return gr.themes.Soft()

        def update_font_size(size):
            return gr.themes.Soft(font=(gr.themes.GoogleFont("Roboto"), f"{size}px"))

        theme_dropdown.change(update_theme, inputs=[theme_dropdown], outputs=[demo])
        font_size_slider.change(update_font_size, inputs=[font_size_slider], outputs=[demo])

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(show_error=True)  # Enable verbose error reporting

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True)
