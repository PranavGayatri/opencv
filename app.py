import streamlit as st
import pandas as pd
import os
from parser import extract_info_from_resume
from gmail_fetcher import fetch_resumes_from_gmail

st.set_page_config(page_title="Resume Parser", layout="wide")
st.title("📄 Resume Parser with Gmail Integration")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
resume_data = []

if st.button("Fetch from Gmail"):
    fetched_files = fetch_resumes_from_gmail("credentials.json")
    uploaded_files = list(uploaded_files) + fetched_files

if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        info = extract_info_from_resume(f"uploads/{uploaded_file.name}")
        info["Filename"] = uploaded_file.name
        resume_data.append(info)

    df = pd.DataFrame(resume_data)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "shortlist.csv")