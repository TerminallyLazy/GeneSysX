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

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=0)

header = """
<div class="fade-in" style='text-align: center;'>
    <h1>🧬 GeneSys AI 🧬</h1>
</div>
"""

subheader = """
<div class="fade-in" style='text-align: center;'>
    <p><em>Making it as easy as AUG</em></p>
</div>
"""

# Inject custom CSS and content
st.markdown(
    f"""
    <style>
        .fade-in {{
            opacity: 0;
            animation: fade-in 1s ease-in-out forwards;
        }}
        @keyframes fade-in {{
            0% {{
                opacity: 0;
            }}
            100% {{
                opacity: 1;
            }}
        }}
    </style>
    {header}
    {subheader}
    """,
    unsafe_allow_html=True,
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.write("GeneSys AI is your all-in-one genomics and bioinformatics companion, designed to empower a wide range of users, from bioinformaticians and researchers to clinicians and students.")

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    load_dotenv()

    # TODO: We don't need this: We can just have them upload any file instead catch the file type and ask them what we would like them to do. We should aim to have minimize customer interactions until they have what they need.
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

    file = st.file_uploader("Drop a file here")

    data_type = determine_file_type(file)

    if data_type:
        st.write(f"I detected a {data_type} file, what would you like to do?")
    else:
        st.write("Please upload a file to determine its type.")
    # Another reason we don't want this to be our implementation is we are going to hopefully have 10 --> 20 file types in the future. Which will be a lot of ifs.

    if data_type == "FASTA":
        if data_type == "FASTA":
            fasta_file = file

            if fasta_file is not None:
                temp_file_path = os.path.join("/tmp", fasta_file.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(fasta_file.read())

                st.success(
                    f"File uploaded successfully. File path: {temp_file_path}")

        if fasta_file is not None:

            # url = get_s3_url(filename=fasta_file.name)
            # upload_content_to_s3(url, fasta_content)

            user_input = st.text_input("Enter some text:")

            if st.button("Submit"):
                st.write(run_conversation(user_input, temp_file_path))
        else:
            st.write("Please upload a FASTA file.")

    elif data_type == "PDB":
        pdb_file = file

        if pdb_file is not None:
            pdb_content = pdb_file.read().decode("utf-8")
            url = get_s3_url(filename=pdb_file.name)
            upload_content_to_s3(url, pdb_content)

            render_protein_file(pdb_content)

        else:
            st.write("Please upload a PDB file.")

    elif data_type == "CSV":
        csv_file = file

        if csv_file is not None:
            st.write("CSV file uploaded. Displaying DataFrame:")
            df = pd.read_csv(csv_file)

            url = get_s3_url(filename=csv_file.name)
            upload_content_to_s3(url, df.to_csv(StringIO()))

            st.dataframe(df)

            llm = OpenAI(api_token=os.getenv("OPEN_API_KEY"))
            sdf = SmartDataframe(df, config={"llm": llm})

            user_input = st.text_input("What is your request?")

            url = get_s3_url(
                filename=f"ChatSession/query-{str(int(time()))}.txt")
            upload_content_to_s3(url, user_input)

            if user_input:
                st.write("User Input:")
                st.write(user_input)

                response = sdf.chat(user_input)

                st.write("SmartDataframe Response:")
                st.write(response)

                if response == None:
                    st.image("exports/charts/temp_chart.png",
                             caption="Chart Image", use_column_width=True)

        if st.button("Submit"):
            df_json = df.to_json(orient="split")
            st.write(run_conversation(user_input, df_json))
        else:
            st.write("Please upload a CSV file.")
