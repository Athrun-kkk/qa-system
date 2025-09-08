# QA System

A simple Question-Answering (QA) system built with [Streamlit](https://streamlit.io/), [LangChain](https://www.langchain.com/), and [OpenAI](https://platform.openai.com/).  
This project allows you to upload documents and interact with them using natural language queries.  

## Features
- 🔎 Document loading (PDF, DOCX, TXT)
- ✂️ Text chunking with LangChain
- 📦 Vector database with Qdrant
- 🤖 Retrieval-based QA using OpenAI GPT
- 💬 Interactive Streamlit chat UI
- 📜 Support for contextual memory (extendable)

---

## Project Structure
```bash
qa-system/
│── app.py             # Main Streamlit app
│── requirements.txt   # Python dependencies
│── .env               # Environment variables file
│── .gitignore         # Ignored files for git
│── README.md          # Project documentation
│── personal_docs/     # Example folder for documents
```

## Setup
1. Create a virtual environment
```bash
python -m venv venv
```
