import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API URL from .env
API_URL = os.getenv("API_URL")

if not API_URL:
    raise ValueError("API_URL not found in .env file")

st.set_page_config(page_title="Simple RAG Demo", layout="centered")

st.title("🔍 Simple RAG Demo with FastAPI + ChromaDB")




query = st.text_input("Enter your question:")

if st.button("Search") and query:
    with st.spinner("Searching..."):
        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            data = response.json()

            st.subheader("📄 Matched Document")
            st.write(data.get("matched_document", "No document found"))

            st.subheader("📊 Similarity Score")
            st.write(data.get("similarity", "N/A"))

            st.subheader("🧬 Query Embedding Preview (first 20 values)")
            st.write(data.get("query_embedding_preview", "No embedding returned"))

        else:
            st.error("API Error: Unable to get response.")
