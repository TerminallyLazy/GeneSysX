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
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import streamlit_authenticator as stauth

logging.info("Loading External Modules")
# Internal Modules
from genesys.env import load_dotenv
from genesys.visuals import render_protein_file
from genesys.ai import run_conversation
from genesys.DNAToolKit import sequence_type, multiple_sequence_alignment
import genesys.client as cli
from genesys.assistants import research_assistant
from genesys.openai import openai_client as client

# import genesys.eventcreator as ec

# --- USER AUTHENTICATION

names = ["Charlie", "Eshcol", "Sandeep", "Raj", "Ashish"]
usernames = ["charlie", "eshcol", "sandeep", "raj", "ashish"]

# Load hashed passwords

file_path = Path("genesys/hashed_pw.pkl")
logging.info("Load hashed passwords")
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# authenticator = stauth.Authenticate(
#     names, usernames, hashed_passwords, "sales_dashboard", "abcdef", cookie_expiry_days=0)

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

st.title('Streamlit Sidebar with Card Output')

st.sidebar.title('Input Sidebar')

user_input = st.sidebar.text_input("Enter your input here")



with st.sidebar.container():
    st.sidebar.markdown("### Your Input")
    st.sidebar.text_area("Input entered:", user_input, height=100)

# name, authentication_status, username = authenticator.login("Login", "main")
username = "charlie"

logging.info("Create Session for Event Creator")
# Initialize Session.
unix_time = str(int(time()))
session_id = f"session-{unix_time}"
# cur_session = # ec.create_session(session_id, username)

logging.info("Loading Temp Directory")
# Different ways of handling local temp directory. 
if os.name == 'nt':  # Windows
    temp_dir = os.getenv('TEMP')
else:  # UNIX-like OS (Mac & Linux)
    temp_dir = "/tmp"

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:
#     authenticator.logout("Logout", "sidebar")
#     st.sidebar.title(f"Welcome {name}")
#     st.sidebar.write("GeneSys AI is your all-in-one genomics and bioinformatics companion, designed to empower a wide range of users, from bioinformaticians and researchers to clinicians and students.")

#     st.sidebar.title(f"Instructions")
#     st.sidebar.write(
#         """
#         1. Upload file.
#         2. Ask a question about your data.
#         3. Get an answer.
#     """
#     )

load_dotenv()

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

logging.info("Uploading a File")
file = st.file_uploader("Drop a file here")

data_type = determine_file_type(file)

if data_type:
    st.write(f"What would you like to do?")
else:
    st.write("Upload a file to get started.")
# Another reason we don't want this to be our implementation is we are going to hopefully have 10 --> 20 file types in the future. Which will be a lot of ifs.

if data_type == "FASTA":
    if data_type == "FASTA":
        fasta_file = file

        if fasta_file is not None:
            filename = f"{str(int(time()))}-{fasta_file.name}"
            temp_file_path = os.path.join(temp_dir, filename)
            logging.info("Opening File path")
            with open(temp_file_path, "wb") as temp_file:
                        fasta_content = fasta_file.read()
                        temp_file.write(fasta_content)

                        fasta_content_str = fasta_content.decode('utf-8')

            cli.upload_s3(fasta_content_str, username, filename, "FASTA")    

            st.success(f"File uploaded successfully!")

if fasta_file is not None:

        # url = get_s3_url(filename=fasta_file.name)
        # upload_content_to_s3(url, fasta_content)

        user_input = st.chat_input("")

        col1, col2 = st.columns(2)

        if user_input:
            st.write(run_conversation(user_input, temp_file_path))
            # ec.create_message_event(username, cur_session, user_input)

        sequence_type = sequence_type(temp_file_path)

        with col1:
            msa_button = None
            orf_button = None
            restriction_button = None
            translate_button = None
            gc_button = None
            isoelectric_button = None
            if sequence_type == "DNA":
                orf_button = st.button("What are the open reading frames?")
                restriction_button = st.button("Find restriction sites on the first sequence")
            elif sequence_type == "RNA":
                translate_button = st.button("Translate the given sequence")
                gc_button = st.button("Calculate the GC content(s)")
            elif sequence_type == "Protein":
                msa_button = st.button("Perform MSA")
                isoelectric_button = st.button("Calculate isoelectric points")

        with col2:
            mass_button = None
            transcription_button = None
            reverse_button = None
            complement_button = None
            phylogenetic_button = None

            if sequence_type == "DNA":
                mass_button = st.button("What is the mass of the given sequence?")
                transcription_button = st.button("Generate the mRNA transcript")
            elif sequence_type == "RNA":
                reverse_button = st.button("Reverse the given sequence")
                complement_button = st.button("Generate the complement(s)")
            elif sequence_type == "Protein":
                mass_button = st.button("What is the mass of the given sequence?")
                phylogenetic_button = st.button("Generate a phylogenetic tree")
                
        #TODO: This should be a list of buttons with a for loop
        # There should be some streamlit class which callsback when a button is pressed and we perform an action based of that button. 
        # This should instead be a dictionary or json structure in another file which has the name of the button & the message of the button. 
        # This will make it easier to add more buttons and remove others cause you just change the dictionary/json. (List of dictionaries)

        if msa_button:
            msa_result = multiple_sequence_alignment(temp_file_path)
            if msa_result:
                st.code(msa_result, language="text")
                # ec.create_response_event(username, cur_session, msa_result, "code", "text")
        elif mass_button:
            st.write(run_conversation("Calculate the mass?", temp_file_path))
            # ec.create_message_event(username, cur_session, "Calculate the mass?")
        elif orf_button:
            st.write(run_conversation("What are the ORFs for the given file?", temp_file_path))
            # ec.create_message_event(username, cur_session, "What are the ORFs for the given file?")
        elif restriction_button:
            st.write(run_conversation("What are restriction sites on the first sequence?", temp_file_path))
            # ec.create_message_event(username, cur_session, "What are restriction sites on the first sequence?")
        elif transcription_button:
            st.write(run_conversation("Generate the mRNA transcript", temp_file_path))
            # ec.create_message_event(username, cur_session, "Generate the mRNA transcript")
        elif translate_button:
            st.write(run_conversation("Translate the given sequence", temp_file_path))
            # ec.create_message_event(username, cur_session, "Translate the given sequence")
        elif gc_button:
            st.write(run_conversation("Calculate the GC content(s)", temp_file_path))
            # ec.create_message_event(username, cur_session, "Calculate the GC content(s)")
        elif reverse_button:
            st.write(run_conversation("Find the reverse complementary", temp_file_path))
            # ec.create_message_event(username, cur_session, "Find the reverse complementary")
        elif complement_button:
            st.write(run_conversation("Generate the complement of the given sequence", temp_file_path))
            # ec.create_message_event(username, cur_session, "Generate the complement of the given sequence")
        elif isoelectric_button:
            st.write(run_conversation("What are the isoelectric points?", temp_file_path))
            # ec.create_message_event(username, cur_session, "What are the isoelectric points?")
        elif phylogenetic_button:
            st.write(run_conversation("Generate a phylogenetic tree", temp_file_path))
            # ec.create_message_event(username, cur_session, "Generate a phylogenetic tree")

        if user_input == None:
            st.write("Ask away!")
            # ec.create_message_event(username, cur_session, "Ask away!")
        else:
            st.write(f"Your question: {user_input}")

elif data_type == "PDB":
    pdb_file = file

    if pdb_file is not None:
        pdb_content = pdb_file.read().decode("utf-8")

        pdb_filename = str(int(time()))+pdb_file.name
        cli.upload_s3(pdb_content, username, pdb_filename, "pdb")
        # ec.create_pdb_event(username, cur_session, pdb_filename, "Visualization")

        pdb_user_input = st.chat_input("")

        if pdb_user_input:
            st.write(render_protein_file(pdb_content)) # TODO: What is this??????! This section makes zero sense why would we wait for the user to type something? This was also purposefully changed from my original implementation which was much simpler.

        st.write(pdb_user_input)

    else:
        st.write("Please upload a PDB file.")
        # ec.create_response_event(username, cur_session, "Please upload a PDB file.")

elif data_type == "CSV":
    csv_file = file

    if csv_file is not None:
        st.write("CSV file uploaded. Displaying DataFrame:")
        # ec.create_response_event(username, cur_session, "CSV file uploaded. Displaying DataFrame:")

        df = pd.read_csv(csv_file)
        csv_filename = str(int(time()))+csv_file.name
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        cli.upload_s3(csv_buffer.getvalue(), username, csv_filename, "csv")
        # ec.create_csv_event(username, cur_session, csv_filename, df)

        st.dataframe(df)
        # ec.display_csv_event(username, cur_session, csv_filename)


    from pandasai.schemas.df_config import Config

    default_config = Config()
    sdf = SmartDataframe(df, config=default_config)

    csv_user_input = st.chat_input("")

    col1, col2 = st.columns(2)


    with col1:
        shape_button = st.button("What is the shape of the dataframe?")
        columns_button = st.button("What are the columns of the dataframe?")
    with col2:
        describe_button = st.button("Tell me the descriptive statistics")
        head_button = st.button("Show the first 5 rows of the dataframe")

        # TODO: These if statements can be simplified so much. I don't think the buttons should be generated in this app. The app file should be a simple loop of user event --> compute event. This architecture is un
        if shape_button:
            csv_user_input = "What is the shape of the dataframe?"
        elif columns_button:
            csv_user_input = "What are the columns of the dataframe?"
        elif describe_button:
            csv_user_input = "Tell me the descriptive statistics of the dataframe"
        elif head_button:
            csv_user_input = "Show the first 5 rows of the dataframe"
        
        
        st.write(csv_user_input)
        # ec.create_message_event(username, cur_session, csv_user_input)

        if csv_user_input:
            st.write(csv_user_input)
            # ec.create_message_event(username, cur_session, csv_user_input)

            response = sdf.chat(csv_user_input)
            # # ec.create_message_event(username, cur_session, response)
            st.write(response)

            if response == None:
                st.image("exports/charts/temp_chart.png",
                            caption="Chart Image", use_column_width=True)
                
