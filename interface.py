import streamlit as st
from ai import run_conversation

st.title("GenomeAI")

fasta_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "txt"])

if fasta_file is not None:
    fasta_content = fasta_file.read().decode("utf-8")
    user_input = st.text_input("Enter some text:")

    if st.button("Submit"):
        st.write(run_conversation(user_input, fasta_content))
else:
    st.write("Please upload a FASTA file.")
