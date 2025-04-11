
#  Web-powered AI Answer Assistant

This Streamlit app uses **SERP API**, **OpenAI**, **BeautifulSoup**, **FAISS**, and **newspaper3k** to fetch and process content from top Google search results, then answers your question using GPT-4 based on that data.

---

##  Features

- 🔎 Fetches Google search results using SERP API
- 📰 Scrapes and extracts meaningful text from top pages
- 🧠 Embeds text using OpenAI's Embedding API
- 📚 Creates a FAISS vector index to find relevant info
- 🤖 Uses GPT-4 to answer your question based on search content

---

##  Project Structure

```
.
├── app.py                    # Main Streamlit app
├── requirements.txt          # All required dependencies
└── .streamlit/
    └── secrets.toml          # API keys stored securely
```

---

##  How It Works (Code Breakdown)

### 1. `get_search_results()`
Uses [SERP API](https://serpapi.com/) to fetch top Google search result URLs for your query.

### 2. `scrape_article()`
Attempts to scrape and clean readable content using:
- `newspaper3k` for structured parsing
- Fallback to `BeautifulSoup` if newspaper fails

### 3. `chunk_text()`
Splits scraped text into small chunks (default 500 words) to fit OpenAI's input limits.

### 4. `embed_texts()`
Embeds each chunk using OpenAI's `text-embedding-3-small` model.

### 5. `build_faiss_index()`
Builds a FAISS similarity index using the text embeddings.

### 6. `search_faiss()`
Finds the top 5 most relevant text chunks using cosine similarity.

### 7. `ask_gpt()`
Sends relevant chunks along with your query to GPT-4 to generate a final answer.

### 8. `Streamlit UI`
Takes user input, triggers scraping + indexing + answering, and displays:
- 📌 Final Answer
- 📄 Context snippets

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/web-powered-ai-assistant.git
cd web-powered-ai-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate      # On Windows (Git Bash)
# OR
source venv/bin/activate          # On macOS/Linux
```
##  Requirements

All dependencies are listed in `requirements.txt`. To generate this file:

```bash
pip freeze > requirements.txt
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Create a `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "your-openai-api-key"
SERP_API_KEY = "your-serp-api-key"
```

### 5. Run the app

```bash
streamlit run app.py
```

---

##  License

MIT License

---

##  Want to contribute?

Pull requests, suggestions, and stars are welcome! ⭐
