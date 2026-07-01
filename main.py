import os
import streamlit as st
import pickle
import time
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially nvidia api key)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="InsightRAG",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Header layout
# ---------------------------------------------------------------------------
with st.container():
    st.markdown("# 🗞️ InsightRAG")
    st.markdown(
        "#### Ask questions across multiple news articles and get sourced, "
        "AI-generated answers."
    )
    st.caption("⚡ Powered by NVIDIA AI Endpoints · LangChain · FAISS")
    st.divider()

# ---------------------------------------------------------------------------
# Sidebar — URL input
# ---------------------------------------------------------------------------
st.sidebar.title("News Article URLs")
st.sidebar.divider()
st.sidebar.info(
    "**How to use**\n\n"
    "1. Paste up to 3 article URLs below.\n"
    "2. Click **Process URLs** to scrape & index them.\n"
    "3. Ask a question in the main panel to get a sourced answer.",
    icon="💡",
)

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}", placeholder="https://example.com/article")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs", type="primary", use_container_width=True)
file_path = "faiss_store.pkl"

llm = ChatNVIDIA(model="meta/llama3-8b-instruct", temperature=0.9, max_tokens=500)

# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------
if process_url_clicked:
    valid_urls = [u for u in urls if u.strip()]

    if not valid_urls:
        st.warning("⚠️ Please enter at least one URL before processing.", icon="⚠️")
    else:
        start_time = time.time()
        with st.status("Processing articles...", expanded=True) as status:
            # load data
            st.write("🔎 Scraping articles...")
            loader = UnstructuredURLLoader(urls=valid_urls)
            data = loader.load()

            # split data
            st.write("✂️ Splitting text into chunks...")
            text_splitter = RecursiveCharacterTextSplitter(
                separators=["\n\n", "\n", ".", ","],
                chunk_size=1000,
            )
            docs = text_splitter.split_documents(data)

            # create embeddings and save it to FAISS index
            st.write("🧠 Generating NVIDIA embeddings...")
            embeddings = NVIDIAEmbeddings(model="NV-Embed-QA")

            st.write("🗄️ Building vector database...")
            vectorstore_nvidia = FAISS.from_documents(docs, embeddings)

            # Save the FAISS index to a pickle file
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_nvidia, f)

            status.update(label="✅ Processing complete!", state="complete", expanded=False)

        elapsed = time.time() - start_time

        # Success metrics
        st.success("Articles processed and indexed successfully!", icon="🎉")
        col1, col2, col3 = st.columns(3)
        col1.metric("URLs Loaded", len(valid_urls))
        col2.metric("Text Chunks", len(docs))
        col3.metric("Processing Time", f"{elapsed:.1f}s")

# ---------------------------------------------------------------------------
# Question & Answer
# ---------------------------------------------------------------------------
st.subheader("💬 Ask a Question")
query = st.text_input("Question:", placeholder="What are the key takeaways from these articles?")

if query:
    if os.path.exists(file_path):
        with st.spinner("Searching articles and generating an answer..."):
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
                chain = RetrievalQAWithSourcesChain.from_llm(
                    llm=llm, retriever=vectorstore.as_retriever()
                )
                result = chain({"question": query}, return_only_outputs=True)
                # result -> {"answer": "", "sources": [] }

        # Answer card
        with st.container(border=True):
            st.markdown("### 📝 Answer")
            st.markdown(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.divider()
                st.markdown("##### 🔗 Sources")
                sources_list = [s for s in sources.split("\n") if s.strip()]
                for source in sources_list:
                    st.markdown(f"- {source}")
    else:
        st.info("Process some article URLs first to build the knowledge base.", icon="ℹ️")
