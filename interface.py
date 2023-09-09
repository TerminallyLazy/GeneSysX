import streamlit as st
import pandas as pd
from ai import run_conversation

st.title("GenomeAI")

data_type = st.radio("Select the type of data to upload:", ["FASTA", "CSV", "PDF"])

if data_type == "FASTA":
    fasta_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "txt"])

    if fasta_file is not None:
        fasta_content = fasta_file.read().decode("utf-8")
        user_input = st.text_input("Enter some text:")

        if st.button("Submit"):
            st.write(run_conversation(user_input, fasta_content))
    else:
        st.write("Please upload a FASTA file.")

elif data_type == "CSV":
    csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if csv_file is not None:
        st.write("CSV file uploaded. Displaying DataFrame:")
        
        # CSV --> DF
        df = pd.read_csv(csv_file)
        st.dataframe(df)

elif data_type == "PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.write("PDF file uploaded. Add your processing logic.")
