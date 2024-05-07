import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import gen
from src.mcqgenerator.logger import logging

with open('Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

#Creating a title
st.title("MCQ Generator using LangChain and Llama2")

#Creating a form for the app
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = gen({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")

                quiz = response.get("quiz")
                if quiz:
                    table_data = get_table_data(quiz)
                    if table_data:
                        df = pd.DataFrame(table_data)
                        df.index += 1
                        st.table(df)
                        st.text_area("Review", value=response.get("review", ""))
                    else:
                        st.error("Failed to parse quiz data.")
                else:
                    st.error("No quiz generated. Please try again.")
            except Exception as e:
                st.error(f"Failed to generate MCQs: {str(e)}")
