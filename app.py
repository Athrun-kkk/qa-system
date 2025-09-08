# app.py
import os
import logging
from dotenv import load_dotenv
import streamlit as st

# ==== Env & logging ====
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==== LangChain imports ====
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# ---- Sidebar controls ----
st.set_page_config(page_title="QA Chatbot", page_icon="💐", layout="wide")
st.sidebar.header("Settings")
temperature = st.sidebar.slider("LLM temperature", 0.0, 1.0, 0.0, 0.1)
top_k = st.sidebar.slider("Retriever top_k", 1, 10, 3, 1)
base_dir = st.sidebar.text_input("Documents folder", "./personal_docs")
st.sidebar.caption("Put your PDF/DOCX/TXT files in this folder.")

# ==== Load documents (safe & optional) ====
documents = []
if os.path.isdir(base_dir):
    for fname in os.listdir(base_dir):
        fpath = os.path.join(base_dir, fname)
        try:
            if fname.lower().endswith(".pdf"):
                documents.extend(PyPDFLoader(fpath).load())
            elif fname.lower().endswith(".docx"):
                documents.extend(Docx2txtLoader(fpath).load())
            elif fname.lower().endswith(".txt"):
                documents.extend(TextLoader(fpath, encoding="utf-8").load())
        except Exception as e:
            logger.warning("Failed to load %s: %s", fpath, e)
else:
    st.sidebar.warning(f"Folder not found: {base_dir}")

# ==== Split text ====
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunked_docs = splitter.split_documents(documents) if documents else []

# ==== Vector store (in-memory Qdrant) ====
embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY from env
if chunked_docs:
    vectorstore = Qdrant.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        location=":memory:",
        collection_name="my_documents",
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
else:
    vectorstore = None
    retriever = None

# ==== LLM & memory ====
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    output_key="answer",
    return_messages=True,
)

# ==== Chain (Conversational RAG) ====
if retriever:
    retrieval_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer",
    )
else:
    retrieval_chain = None

# ==== UI ====
st.title("QA Chatbot (Context Memory + RAG)")
st.caption("Ask questions about your documents. The bot remembers the conversation.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [{'user':..., 'bot':..., 'sources':[...]}]

# Input form to enable Enter-to-send
with st.form("chat_form"):
    question = st.text_input("Type your question:", "")
    submitted = st.form_submit_button("Send")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    elif retrieval_chain is None:
        st.error("No documents loaded or retriever not available. Add files to the folder and rerun.")
    else:
        try:
            result = retrieval_chain({"question": question})
            answer = result.get("answer", "")
            sources = result.get("source_documents", []) or []
            st.session_state.chat_history.append({
                "user": question,
                "bot": answer,
                "sources": [
                    {
                        "source": os.path.basename(doc.metadata.get("source", "unknown")),
                        "page": doc.metadata.get("page"),
                        "preview": doc.page_content[:200].replace("\n", " ")
                    }
                    for doc in sources
                ]
            })
        except Exception as e:
            logger.exception("Error while answering")
            st.session_state.chat_history.append({
                "user": question,
                "bot": f"System error: {e}",
                "sources": []
            })

# Render chat
for i, chat in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
    if chat.get("sources"):
        with st.expander("Sources"):
            for j, s in enumerate(chat["sources"], start=1):
                src_line = f"{j}. {s['source']}"
                if s.get("page") is not None:
                    src_line += f" (page {s['page']})"
                st.write(src_line)
                st.caption(s["preview"] + ("..." if len(s["preview"]) == 200 else ""))
    st.markdown("---")
