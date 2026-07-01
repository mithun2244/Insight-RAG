import os
import streamlit as st
import pickle
import time
import requests
import trafilatura
from langchain_core.documents import Document
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially nvidia api key)

# A realistic browser User-Agent helps bypass basic bot-blocking (HTTP 403).
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def load_articles(urls, timeout=20):
    """Fetch each URL and extract its main article text.

    Uses requests (with a browser User-Agent) to fetch the HTML, then
    trafilatura to pull out the clean article body — far faster and more
    robust than parsing full pages. Returns (documents, failures) where
    failures is a list of (url, reason) tuples for anything that couldn't
    be loaded.
    """
    documents, failures = [], []
    for url in urls:
        try:
            resp = requests.get(url, headers=BROWSER_HEADERS, timeout=timeout)
            if resp.status_code != 200:
                failures.append((url, f"HTTP {resp.status_code}"))
                continue
            text = trafilatura.extract(resp.text, include_comments=False, include_tables=False)
            if not text or not text.strip():
                failures.append((url, "no extractable article text"))
                continue
            documents.append(Document(page_content=text.strip(), metadata={"source": url}))
        except Exception as exc:  # network errors, timeouts, etc.
            failures.append((url, type(exc).__name__))
    return documents, failures

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

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0.9, max_tokens=500)

# ---------------------------------------------------------------------------
# Processing pipeline
# ---------------------------------------------------------------------------
if process_url_clicked:
    valid_urls = [u for u in urls if u.strip()]

    if not valid_urls:
        st.warning("⚠️ Please enter at least one URL before processing.", icon="⚠️")
    else:
        start_time = time.time()
        data, failures = [], []
        with st.status("Processing articles...", expanded=True) as status:
            # load data
            st.write("🔎 Scraping articles...")
            data, failures = load_articles(valid_urls)

            if not data:
                status.update(label="❌ No articles could be loaded", state="error")
            else:
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

        # Report any URLs that could not be scraped
        for url, reason in failures:
            st.warning(f"Skipped **{url}** — {reason}", icon="⚠️")

        if data:
            elapsed = time.time() - start_time

            # Success metrics
            st.success("Articles processed and indexed successfully!", icon="🎉")
            col1, col2, col3 = st.columns(3)
            col1.metric("Articles Loaded", len(data))
            col2.metric("Text Chunks", len(docs))
            col3.metric("Processing Time", f"{elapsed:.1f}s")
        else:
            st.error(
                "None of the provided URLs could be scraped. The sites may block "
                "automated access or contain no extractable article text. Try a "
                "different source.",
                icon="🚫",
            )

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
