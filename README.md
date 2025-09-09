# QA System with RAG

A simple Question-Answering (QA) system based on RAG built with [Streamlit](https://streamlit.io/), [LangChain](https://www.langchain.com/), and [OpenAI](https://platform.openai.com/).  
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
2. Activate it
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Open .env and add your API keys
```bash
# OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```
5. Add documents
Place your PDF, DOCX, or TXT files inside the below folder
```bash
./personal_docs/
```


6. Run the Streamlit app
```bash
streamlit run app.py
```
7. Open in browser
By default, the app runs at:
```bash
http://localhost:8501
```

