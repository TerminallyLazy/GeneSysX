# Standard Library
import os
from io import StringIO
from time import time
import random
import pickle
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logging.info("Loading External Modules")
# External Modules
from pathlib import Path
import gradio as gr
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.schemas.df_config import Config

logging.info("Loading Internal Modules")
# Internal Modules
from genesys.env import load_dotenv
from genesys.visuals import render_protein_file
from genesys.ai import run_conversation
from genesys.DNAToolKit import sequence_type, multiple_sequence_alignment
import genesys.client as cli
from genesys.assistants import research_assistant
from genesys.openai import openai_client as client

# Load environment variables
load_dotenv()

# --- USER AUTHENTICATION
username = "charlie"  # For demonstration purposes

logging.info("Creating Temp Directory")
# Different ways of handling local temp directory.
if os.name == 'nt':  # Windows
    temp_dir = os.getenv('TEMP')
else:  # UNIX-like OS (Mac & Linux)
    temp_dir = "/tmp"

logging.info("Determining File Type")
def determine_file_type(file):
    if file is not None:
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == "fasta":
            return "FASTA"
        elif file_extension == "csv":
            return "CSV"
        elif file_extension == "pdb":
            return "PDB"
    return None

def process_file(file):
    if file is not None:
        data_type = determine_file_type(file)
        filename = f"{str(int(time()))}-{file.name}"
        temp_file_path = os.path.join(temp_dir, filename)
        with open(temp_file_path, "wb") as temp_file:
            content = file.read()
            temp_file.write(content)
        content_str = content.decode('utf-8')
        cli.upload_s3(content_str, username, filename, data_type)
        return data_type, temp_file_path, content_str
    return None, None, None

def run_analysis(analysis_type, temp_file_path):
    return run_conversation(analysis_type, temp_file_path)

def create_gradio_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# 🧬 GeneSys AI 🧬")
        gr.Markdown("*Making it as easy as AUG*")

        with gr.Row():
            with gr.Column():
                file_upload = gr.File(label="Drop a file here")
                data_type_output = gr.Textbox(label="File Type")
                process_button = gr.Button("Process File")

            with gr.Column():
                chat_input = gr.Textbox(label="Ask a question about your data")
                chat_output = gr.Textbox(label="Answer")
                chat_button = gr.Button("Ask")

        with gr.Row():
            with gr.Column():
                dna_buttons = [
                    gr.Button("What are the open reading frames?"),
                    gr.Button("Find restriction sites on the first sequence"),
                    gr.Button("What is the mass of the given sequence?"),
                    gr.Button("Generate the mRNA transcript")
                ]
            with gr.Column():
                rna_buttons = [
                    gr.Button("Translate the given sequence"),
                    gr.Button("Calculate the GC content(s)"),
                    gr.Button("Reverse the given sequence"),
                    gr.Button("Generate the complement(s)")
                ]
            with gr.Column():
                protein_buttons = [
                    gr.Button("Perform MSA"),
                    gr.Button("Calculate isoelectric points"),
                    gr.Button("What is the mass of the given sequence?"),
                    gr.Button("Generate a phylogenetic tree")
                ]

        analysis_output = gr.Textbox(label="Analysis Result")

        def process_and_analyze(file, analysis_type=None):
            data_type, temp_file_path, content = process_file(file)
            if data_type:
                if analysis_type:
                    return run_analysis(analysis_type, temp_file_path)
                return f"File processed. Type: {data_type}"
            return "No file uploaded or processing failed"

        process_button.click(process_and_analyze, inputs=[file_upload], outputs=[data_type_output])
        chat_button.click(process_and_analyze, inputs=[file_upload, chat_input], outputs=[chat_output])

        for button in dna_buttons + rna_buttons + protein_buttons:
            button.click(process_and_analyze, inputs=[file_upload], outputs=[analysis_output],
                         api_name=lambda b=button: f"analyze_{b.label.lower().replace(' ', '_')}")

        def render_protein(file):
            _, _, content = process_file(file)
            if content:
                return render_protein_file(content)
            return "No PDB file uploaded or processing failed"

        protein_vis_button = gr.Button("Visualize Protein")
        protein_vis_output = gr.HTML(label="Protein Visualization")
        protein_vis_button.click(render_protein, inputs=[file_upload], outputs=[protein_vis_output])

        def analyze_csv(file, query):
            _, temp_file_path, _ = process_file(file)
            if temp_file_path:
                df = pd.read_csv(temp_file_path)
                sdf = SmartDataframe(df, config=Config())
                return sdf.chat(query)
            return "No CSV file uploaded or processing failed"

        csv_buttons = [
            gr.Button("What is the shape of the dataframe?"),
            gr.Button("What are the columns of the dataframe?"),
            gr.Button("Tell me the descriptive statistics"),
            gr.Button("Show the first 5 rows of the dataframe")
        ]

        csv_output = gr.Textbox(label="CSV Analysis Result")

        for button in csv_buttons:
            button.click(analyze_csv, inputs=[file_upload, gr.Textbox(visible=False, value=button.label)], outputs=[csv_output],
                         api_name=f"analyze_csv_{button.label.lower().replace(' ', '_')}")

    return interface

interface = create_gradio_interface()
interface = create_gradio_interface()
