import gradio as gr
import os
from genesys.ai import run_conversation
from genesys.visuals import create_protein_interface
from genesys.client import upload_s3
from dotenv import load_dotenv

load_dotenv()

def process_file(file):
    file_path = file.name
    file_type = file.name.split('.')[-1].upper()
    return f"File processed: {file_path}, Type: {file_type}"

def answer_question(question, file):
    file_path = file.name
    return run_conversation(question, file_path)

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
