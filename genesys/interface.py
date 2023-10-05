# External Modules
import pickle
from pathlib import Path

import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

import streamlit_authenticator as stauth

# Internal Modules
from protein_render import render_protein_file
from ai import run_conversation
from client import upload_content_to_s3, get_s3_url

# Standard Library
import os
from env import load_dotenv
import logging
from io import StringIO
from time import time

# --- USER AUTHENTICATION

names = ["Charlie", "Eshcol", "Sandeep", "Raj", "Ashish"]
usernames = ["charlie", "eshcol", "sandeep", "raj", "ashish"]

# Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    load_dotenv()

    st.title("🧬 GeneSys AI 🧬") # TODO: Center this.

    data_type = st.radio("Select the type of data to upload:", ["FASTA", "CSV", "PDF", "PDB"]) # TODO: We don't need this: We can just have them upload any file instead catch the file type and ask them what we would like them to do. We should aim to have minimize customer interactions until they have what they need.
    # Another reason we don't want this to be our implementation is we are going to hopefully have 10 --> 20 file types in the future. Which will be a lot of ifs.


    if data_type == "FASTA":
        fasta_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "txt"])

        if fasta_file is not None:

            fasta_content = fasta_file.read().decode("utf-8")
            url = get_s3_url(filename=fasta_file.name)
            upload_content_to_s3(url, fasta_content)

            user_input = st.text_input("Enter some text:")

            if st.button("Submit"): 
                st.write(run_conversation(user_input, fasta_content))
        else:
            st.write("Please upload a FASTA file.")

    elif data_type == "PDB": 
        pdb_file = st.file_uploader("Upload a FASTA file", type=["pdb" , "txt"])

        if pdb_file is not None:
            pdb_content = pdb_file.read().decode("utf-8")
            url = get_s3_url(filename=pdb_file.name)
            upload_content_to_s3(url, pdb_content)

            render_protein_file(pdb_content)

        else:
            st.write("Please upload a FASTA file.")

    elif data_type == "CSV":
        csv_file = st.file_uploader("Upload a CSV file", type=["csv", "txt"])

        if csv_file is not None:
            st.write("CSV file uploaded. Displaying DataFrame:")
            df = pd.read_csv(csv_file)

            url = get_s3_url(filename=csv_file.name)
            upload_content_to_s3(url, df.to_csv(StringIO()))

            st.dataframe(df)

            llm = OpenAI(api_token=os.getenv("OPEN_API_KEY"))
            sdf = SmartDataframe(df, config={"llm": llm})

            user_input = st.text_input("What is your request?")

            url = get_s3_url(filename=f"ChatSession/query-{str(int(time()))}.txt")
            upload_content_to_s3(url, user_input)

            if user_input:
                st.write("User Input:")
                st.write(user_input)

                response = sdf.chat(user_input)

                st.write("SmartDataframe Response:")
                st.write(response)

                if response == None:
                    st.image("exports/charts/temp_chart.png", caption="Chart Image", use_column_width=True)


        if st.button("Submit"):
            df_json = df.to_json(orient="split")
            st.write(run_conversation(user_input, df_json))
        else:
            st.write("Please upload a FASTA file.")

    elif data_type == "PDF":
        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

        if pdf_file is not None:
            st.write("PDF file uploaded. Add your processing logic.")
            # url = get_s3_url(pdf_file)
            # upload_content_to_s3(url, pdf_content.name)
