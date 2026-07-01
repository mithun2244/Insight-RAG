# 🗞️ News Research Tool

**News Research Tool** is a user-friendly application for effortless information retrieval across news articles. Paste in article URLs, ask questions in natural language, and receive concise, sourced answers — now supercharged by **NVIDIA AI Endpoints**.

> ⚡ **New system upgrade:** This project has migrated from OpenAI to **NVIDIA AI Endpoints**, using the **`meta/llama3-8b-instruct`** model for generation and **NVIDIA Embeddings (`NV-Embed-QA`)** for semantic search — paired with a redesigned, premium Streamlit dashboard.

---

## 🎨 Interface Transformation

The UI has been completely redesigned for a cleaner, more premium experience. See the before and after below:

| Old UI | New UI |
|:------:|:------:|
| _<!-- Drop your OLD UI screenshot here, e.g. ![Old UI](docs/old_ui.png) -->_ | _<!-- Drop your NEW UI screenshot here, e.g. ![New UI](docs/new_ui.png) -->_ |
| **Before** — basic layout, plain text status | **After** — animated status steps, success metrics & card-style answers |

> 💡 Tip: Add your images to a `docs/` folder (or the project root) and replace the placeholder comments above with `![Old UI](path)` and `![New UI](path)`.

---

## ✨ Features

- Load one or more article URLs to fetch and process content.
- Process article content through LangChain's `UnstructuredURLLoader`.
- Construct embedding vectors using **NVIDIA Embeddings (`NV-Embed-QA`)** and leverage **FAISS**, a powerful similarity search library, for swift and effective retrieval of relevant information.
- Interact with the **NVIDIA-hosted `meta/llama3-8b-instruct` LLM** by inputting queries and receiving answers along with source URLs.
- Enjoy a modern dashboard with animated progress indicators, processing metrics, and clean card-style answer presentation.

---

## 🛠️ Tech Stack

- **LLM:** NVIDIA AI Endpoints — `meta/llama3-8b-instruct` (via `ChatNVIDIA`)
- **Embeddings:** NVIDIA — `NV-Embed-QA` (via `NVIDIAEmbeddings`)
- **Framework:** LangChain
- **Vector Store:** FAISS
- **UI:** Streamlit

---

## 🚀 Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/mithun2244/news-research-tool.git
```

2. Navigate to the project directory:

```bash
cd news-research-tool
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

4. Set up your **NVIDIA API key** by creating a `.env` file in the project root and adding your key:

```bash
NVIDIA_API_KEY=your_api_key_here
```

> 🔑 You can generate an API key from the [NVIDIA API Catalog](https://build.nvidia.com/). Keep your `.env` file private — it is excluded from version control via `.gitignore`.

---

## 💻 Usage/Examples

1. Run the Streamlit app by executing:

```bash
streamlit run main.py
```

2. The web app will open in your browser.

- On the sidebar, input up to 3 article URLs directly.
- Initiate data loading and processing by clicking **"Process URLs"**.
- Watch the animated status container as the system scrapes articles, generates NVIDIA embeddings, and builds the vector database.
- Once complete, success metrics display the number of URLs loaded, text chunks created, and processing time.
- The FAISS index is saved to a local pickle file for future use.
- Ask a question and get an answer — presented in a clean card layout — based on those news articles, complete with sources.

Example news articles to try:

- https://www.moneycontrol.com/news/business/tata-motors-mahindra-gain-certificates-for-production-linked-payouts-11281691.html
- https://www.moneycontrol.com/news/business/tata-motors-launches-punch-icng-price-starts-at-rs-7-1-lakh-11098751.html
- https://www.moneycontrol.com/news/business/stocks/buy-tata-motors-target-of-rs-743-kr-choksey-11080811.html

---

## 📂 Project Structure

- `main.py` — The main Streamlit application script.
- `requirements.txt` — A list of required Python packages for the project.
- `faiss_store_openai.pkl` — A pickle file to store the FAISS index.
- `.env` — Configuration file for storing your **NVIDIA API key** (not committed to version control).
