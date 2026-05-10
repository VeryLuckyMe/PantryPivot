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
    """Initialize or load RAG pipeline."""

    if not os.path.exists(PDF_PATH):
        print("⚠️ No knowledge_base.pdf found. RAG disabled.")
        return None

    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ No Gemini API key found for embeddings. RAG disabled.")
            return None

        embedding = GoogleGenerativeAIEmbeddings(
            model="embedding-001", google_api_key=api_key
        )

        # ✅ LOAD existing DB instead of recreating
        if os.path.exists(CHROMA_DIR):
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

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        return retriever

    except Exception as e:
        st.session_state["rag_error"] = str(e)
        print(f"RAG setup failed: {e}")
        return None


def query_rag(query: str) -> str:
    """Retrieve relevant context from vector DB."""
    retriever = setup_rag()

    if not retriever:
        return ""

    try:
        docs = retriever.get_relevant_documents(query)

        if not docs:
            return ""

        # ✅ clean context formatting with citations
        context = "\n\n".join([f"[Source: Page {doc.metadata.get('page', 'Unknown')}]\n{doc.page_content}" for doc in docs[:3]])

        return context

    except Exception as e:
        return ""
