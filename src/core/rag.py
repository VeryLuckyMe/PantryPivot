# ── RAG (Retrieval-Augmented Generation) Pipeline ───────────────────────────
# Loads a PDF knowledge base, splits it into chunks, stores embeddings in
# ChromaDB, and retrieves relevant context for AI recipe generation.

import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

CHROMA_DIR = "./chroma_db"
PDF_PATH = "knowledge_base.pdf"


@st.cache_resource
def setup_rag():
    """Initialize or load RAG pipeline. Returns a dict with 'retriever' or 'error'."""

    if not os.path.exists(PDF_PATH):
        return {"retriever": None, "error": f"File Missing: '{PDF_PATH}' not found in root."}

    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"retriever": None, "error": "API Key Missing: GEMINI_API_KEY not found in secrets."}

        embedding = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", google_api_key=api_key
        )

        # ✅ LOAD existing DB if healthy, otherwise create
        try:
            if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
                vectorstore = Chroma(
                    persist_directory=CHROMA_DIR,
                    embedding_function=embedding
                )
            else:
                loader = PyPDFLoader(PDF_PATH)
                docs = loader.load()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100
                )
                chunks = splitter.split_documents(docs)

                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embedding,
                    persist_directory=CHROMA_DIR
                )
        except Exception as e:
            # If Chroma fails to load (e.g. corruption), try to re-index from scratch
            print(f"ChromaDB error, attempting re-index: {e}")
            loader = PyPDFLoader(PDF_PATH)
            vectorstore = Chroma.from_documents(
                documents=loader.load(),
                embedding=embedding,
                persist_directory=CHROMA_DIR
            )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        return {"retriever": retriever, "error": None}

    except Exception as e:
        error_msg = f"RAG Initialization Failed: {str(e)}"
        print(f"Error: {error_msg}")
        return {"retriever": None, "error": error_msg}


def query_rag(query: str) -> str:
    """Retrieve relevant context from vector DB."""
    rag_result = setup_rag()
    retriever = rag_result.get("retriever")

    if not retriever:
        return ""

    try:
        docs = retriever.invoke(query)

        if not docs:
            return ""

        # ✅ clean context formatting with citations
        context = "\n\n".join([f"[Source: Page {doc.metadata.get('page', 'Unknown')}]\n{doc.page_content}" for doc in docs[:3]])

        return context

    except Exception as e:
        return ""
