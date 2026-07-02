# 🗞️ InsightRAG

🚀 **[Live Demo Available Here](https://insight-rag-c6tw84fxcj5bcvg77frjiu.streamlit.app)**

**InsightRAG** is a premium AI system for effortless information retrieval across news articles. Paste in article URLs, ask questions in natural language, and receive concise, sourced answers — powered by **NVIDIA AI Endpoints**.

Built for speed and clarity, the tool combines state-of-the-art large language models with fast semantic search to turn scattered news content into instant, cited insights.

---

## ✨ Features

- **Web article scraping** — Fetches and extracts clean article text from any URL using `requests` with a browser User-Agent and `trafilatura`, bypassing basic bot-blocking with graceful per-URL failure handling.
- **NVIDIA NIM API text embeddings** — Converts article chunks into dense semantic vectors via NVIDIA NIM (`NV-Embed-QA`), purpose-built for high-quality question-answering retrieval.
- **FAISS vector similarity search** — Indexes embeddings in a FAISS vector store for fast, accurate nearest-neighbour retrieval of the most relevant passages.
- **Sourced AI answers** — Uses the NVIDIA-hosted `meta/llama-3.3-70b-instruct` LLM to generate concise answers, each returned with its source URLs.
- **Modern dashboard** — A polished Streamlit UI with animated progress steps, live processing metrics, and clean card-style answer presentation.

---

## 🛠️ Tech Stack

- **Python** — Core application language.
- **LangChain** — Orchestration of the retrieval-augmented generation pipeline.
- **FAISS** — Vector store for similarity search.
- **Streamlit** — Interactive web UI.
- **NVIDIA AI Endpoints** — LLM (`meta/llama-3.3-70b-instruct`) and embeddings (`NV-Embed-QA`).

---

## ⚙️ Local Setup

Get InsightRAG running on your machine in three steps.

**1. Install the dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure your NVIDIA API key**

Create a `.env` file in the project root and add your key:

```bash
NVIDIA_API_KEY=your_api_key_here
```

> 🔑 You can generate an API key from the [NVIDIA API Catalog](https://build.nvidia.com/). Keep your `.env` file private — it is excluded from version control via `.gitignore`.

**3. Run the app**

```bash
streamlit run main.py
```

The app opens in your browser. Paste up to 3 article URLs in the sidebar, click **Process URLs**, then ask a question to get a sourced answer.

---

## 🎨 User Interface

A clean, premium Streamlit dashboard with animated status steps, live processing metrics, and card-style answers:

![InsightRAG UI](docs/app_screenshot.png)

---

## 📂 Project Structure

- `main.py` — The main Streamlit application script.
- `requirements.txt` — A list of required Python packages for the project.
- `faiss_store.pkl` — A pickle file to store the FAISS index.
- `.env` — Configuration file for storing your **NVIDIA API key** (not committed to version control).

---

## 👤 Author

System architecture designed and built by **Mithun Roy**, AI and Machine Learning Engineer.
