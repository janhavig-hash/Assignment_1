# 🤖 AI-Based Tax Assistant 

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128%2B-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Test Coverage](https://img.shields.io/badge/Coverage-74%25-brightgreen)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

A local, secure AI-powered assistant that analyzes Income Tax documents (Form 16, Salary Slips, ITRs) and answers user queries with high accuracy. 

---

## 🚀 Key Features

* **🔐 Multi-User Session Isolation:** Uses metadata filtering (`session_id`) to ensure users can only query *their own* uploaded documents, preventing data leakage in shared environments.
* **🔑 Encrypted PDF Support:** Automatically detects password-protected PDFs (e.g., Bank Statements) and prompts the user for credentials via the UI.
* **🧠 Local & Secure AI:** Runs entirely offline using **Ollama (Mistral 7B)** and **Nomic Embeddings**, ensuring financial data never leaves the machine.
* **⚡ Production-Ready Backend:** Built with **FastAPI** featuring strict Pydantic validation, CORS security, and centralized configuration management.
* **📄 Advanced Parsing:** Uses `pypdf` with chunking strategies optimized for financial documents (500 chars / 50 overlap).

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn, Python-Multipart
* **Frontend:** Streamlit
* **AI & Embeddings:** Ollama (Mistral 7B), Nomic-Embed-Text
* **Vector Database:** ChromaDB (Local Persistent Storage)
* **Security:** Cryptography (AES Decryption), UUID Session Management
* **Testing:** Pytest, Pytest-Cov, Pytest-HTML, HTTPX

---

## 📂 Project Structure

```text
tax-assistant-ai/
├── app/
│   ├── api/            # Endpoints (upload.py, query.py)
│   ├── core/           # Config (Settings, Logging)
│   ├── services/       # Logic (pdf_service.py, vector_store.py, embedding.py)
│   └── main.py         # App Entry Point
├── data/               # Local storage for Uploads & ChromaDB (Ignored by Git)
├── tests/              # Pytest Unit & Integration Tests
├── frontend.py         # Streamlit User Interface
├── requirements.txt    # Project Dependencies
├── .env.example        # Configuration Template
└── README.md           # Documentation
---
```
## 1.Clone the reposistory 

```
(https://github.com/janhavig-hash/Training_Tasks/tree/main/Task_4_Capstone_project)

```
---
## 2. Create Virtual Environment
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```
---
## 3. Install Dependencies

```
pip install -r requirements.txt
```
---

---
## Terminal 1: Start Backend API   

```
uvicorn app.main:app --reload
# API will start at [http://127.0.0.1:8000](http://127.0.0.1:8000)

```
---

---
## Terminal 2: Start Frontend UI

```
streamlit run frontend.py
# UI will open at http://localhost:8501
```
---

## 💡 Usage Guide

# 1. Uploading Documents
1. Open the web interface at http://localhost:8501.
2.In the sidebar, look for the "Upload Tax Documents" section.
3.Drag and drop your PDF files (e.g., Form 16, ITR, Salary Slips).
4.Click **"Process Documents"**.
      Note: If the document is password-protected, a password field will appear automatically.              Enter the password and click Retry.

## 2. Asking Questions
1.Once processing is complete, go to the Chat Interface in the main window.
2.Type questions in natural language. Examples:
"What is my total taxable income according to Form 16?"
"List all the deductions claimed under Section 80C."
"How much tax have I already paid?"
The AI will retrieve relevant sections from your documents and provide a concise answer.















