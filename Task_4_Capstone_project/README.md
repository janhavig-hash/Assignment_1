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

⚙️ Installation & Setup
Prerequisites:
-Python 3.10+
-Ollama installed and running (ollama pull mistral)

1. Clone the Repository


2.Create Virtual Environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

3.Install Dependencies
pip install -r requirements.txt

🏃‍♂️ How to Run
You need to run the Backend and Frontend in two separate terminals.

Terminal 1: Start Backend API
uvicorn app.main:app --reload
# API will start at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Terminal 2: Start Frontend UI
streamlit run frontend.py
# UI will open at http://localhost:8501

🧪 Running Tests
This project enforces code quality using Pytest.
pytest

Generate Coverage Report:
pytest --cov=app --cov-report=html
# Open htmlcov/index.html to view the report

📝 Usage Guide
1.Open the Streamlit App in your browser.
2.Upload a Tax PDF (e.g., Form 16).
3.Click "Process Document".
4.Ask questions like:
"What is the total taxable income?"
"What was the registered office and leave travel allowances under section 10?"
"What is the basic salary and HRA month for june-23?"



