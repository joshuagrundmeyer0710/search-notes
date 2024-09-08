"""
Filename: eval_chain.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Simple Streamlit application for asking questions and getting answers from an API.

Copyright (c) 2024 Szymon Manduk AI.
"""

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Google Keep Notes Search Engine")

# Input for user question
question = st.text_input("Your question:")

if st.button("Get Answer"):
    if question:
        # Send request to your API
        response = requests.post(f"{API_URL}/answer", json={"question": question})
        if response.status_code == 200:
            answer = response.json()["answer"]
            steps = response.json()["steps"]
            st.write("Answer:", answer)
            st.write("Steps:", steps)
        else:
            st.error("Failed to get an answer. Please try again.")
    else:
        st.warning("Please enter a question.")


st.divider()

# Read the contents of readme.md
with open("readme.md", "r") as f:
    readme_content = f.read()

# Display the contents in Streamlit
st.markdown(readme_content)
