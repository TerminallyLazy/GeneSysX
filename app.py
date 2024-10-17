import gradio as gr
import os
import logging
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
    file_path = file.name
    file_type = file.name.split('.')[-1].upper()
    try:
        if file_type == 'FASTA':
            sequence_type = toolkit.sequence_type(file_path)
            gc_content = toolkit.gc_content(file_path)
            return f"File processed: {file_path}, Type: {file_type}, Sequence Type: {sequence_type}, GC Content: {gc_content:.2f}%"
        elif file_type == 'PDB':
            return f"PDB file processed: {file_path}. Use Protein Visualization tab for further analysis."
        else:
            return f"File processed: {file_path}, Type: {file_type}"
    except Exception as e:
        logging.error(f"Error in process_file: {str(e)}")
        return f"An error occurred while processing the file: {str(e)}"

def answer_question(question, file):
    file_path = file.name
    logging.debug(f"Answering question: '{question}' for file: {file_path}")
    try:
        if question.lower().strip() == "what are the sequence ids in the uploaded fasta file?":
            sequence_ids = toolkit.extract_sequence_ids(file_path)
            answer = f"The sequence IDs in the uploaded FASTA file are: {', '.join(sequence_ids)}"
        else:
            with open(file_path, 'r') as f:
                file_content = f.read()
            answer = run_conversation(question, StringIO(file_content))
        logging.debug(f"Answer received: {answer[:100]}...")  # Log first 100 characters of the answer
        return answer
    except Exception as e:
        logging.error(f"Error in answer_question: {str(e)}")
        return f"An error occurred: {str(e)}"

def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# GeneSysX Gradio App")
        gr.Markdown("## Quick Start Guide")
        gr.Markdown("1. 📤 Upload a file (FASTA, CSV, or PDB)")
        gr.Markdown("2. 🔍 Click 'Process File' to analyze")
        gr.Markdown("3. ❓ Ask a question about the data")
        gr.Markdown("4. 🧬 For PDB files, check the Protein Visualization tab")

        with gr.Tab("File Processing"):
            file_input = gr.File(label="Upload File (FASTA, CSV, or PDB)")
            process_button = gr.Button("Process File")
            output = gr.Textbox(label="Processing Result")

            question_input = gr.Textbox(label="Ask a question about the data")
            answer_button = gr.Button("Get Answer")
            answer_output = gr.Textbox(label="Answer")

            process_button.click(process_file, inputs=[file_input], outputs=[output])
            answer_button.click(answer_question, inputs=[question_input, file_input], outputs=[answer_output])

        with gr.Tab("Protein Visualization"):
            create_protein_interface()

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True)
