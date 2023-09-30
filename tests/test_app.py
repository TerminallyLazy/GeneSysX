import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.middlewares import StreamlitMiddleware
from pandasai.llm import OpenAI

st.title("InsightAI 🔎")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded DataFrame:")
    st.write(df)

    llm = OpenAI(api_token=OPEN_API_KEY)
    sdf = SmartDataframe(df, {"middlewares": [StreamlitMiddleware()]}, config={"llm": llm})

    user_input = st.text_input("What is your request?")

    if user_input:
        st.write("User Input:")
        st.write(user_input)

        response = sdf.chat(user_input)

        st.write("SmartDataframe Response:")
        st.write(response)