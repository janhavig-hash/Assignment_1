# 🤖 AI Tax Assistant (RAG Pipeline)

A local, secure AI-powered assistant that analyzes Income Tax documents (Form 16, Salary Slips) and answers user queries with high accuracy. Built using **Retrieval-Augmented Generation (RAG)** to ensure answers are grounded in the uploaded data, eliminating hallucinations.

## 🚀 Features

* **📄 PDF Parsing:** Automatically extracts text and tables from complex PDF documents (Form 16, Investment Proofs).
* **🧠 RAG Architecture:** Uses Vector Search (ChromaDB) to retrieve only the relevant chunks of data for the LLM.
* **🔒 Local Privacy:** Runs entirely offline using **Ollama** (Mistral), ensuring sensitive financial data never leaves the machine.
* **⚡ Fast API:** Backend built with **FastAPI** for high-performance handling of requests.
* **🖥️ User-Friendly Interface:** **Streamlit** frontend for easy file uploads and chat interactions.
* **✅ Robust Testing:** Includes a comprehensive test suite with **67%+ Code Coverage** (Pytest).

* ## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** Streamlit
* **AI & Search:** Ollama (LLM), ChromaDB (Vector Store), Sentence-Transformers (Embeddings)
* **PDF Processing:** PyPDF, LangChain Text Splitters
* **Testing:** Pytest, Pytest-Cov

* ## 📂 Project Structure
```text
tax-assistant-ai/
├── app/
│   ├── api/            # Endpoints (Upload, Query)
│   ├── core/           # Configuration & Logging
│   ├── db/             # Database Connection (ChromaDB)
│   ├── services/       # Business Logic (PDF, LLM, Embeddings)
│   └── main.py         # App Entry Point
├── data/               # Local storage for Uploads & DB
├── tests/              # Unit and Integration Tests
├── frontend.py         # Streamlit User Interface
├── requirements.txt    # Project Dependencies
└── README.md           # Documentation

