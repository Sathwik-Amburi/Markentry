import streamlit as st
import os
import uuid
from markentry.tools.report_tool import generate_report, save_var_to_md, markdown_to_pdf
from markentry.workflow import graph
from langgraph.types import Command

# Configuration
OUTPUT_DIR = "markentry/outputs"
REPORT_FILE = os.path.join(OUTPUT_DIR, "generate_report.md")

# Set Streamlit page config
st.set_page_config(page_title=" Market Entry Report", page_icon="📄", layout="wide")
st.title("📢 Market Entry Assistant")

# Section 1: Display the latest generated report
if os.path.exists(REPORT_FILE):
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        report_content = file.read()
    st.markdown(report_content, unsafe_allow_html=True)
else:
    st.warning("No report found. Generate a report by asking a question!")

# Section 2: User Input for New Questions
st.header("💬 Ask a New Question")
user_input = st.text_input("Enter your question:", placeholder="e.g., What are the market trends for drones?")
if st.button("Submit Question"):
    st.success("Question submitted successfully!")