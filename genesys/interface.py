import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from API_SECRETS import OPEN_API_KEY
from ai import run_conversation

st.title("🧬 GeneSys AI 🧬")

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
        
        df = pd.read_csv(csv_file)
        st.dataframe(df)

        llm = OpenAI(api_token=OPEN_API_KEY)
        sdf = SmartDataframe(df, config={"llm": llm})

        user_input = st.text_input("What is your request?")

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
