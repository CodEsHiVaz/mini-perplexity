import streamlit as st
import openai
import requests
import faiss
import numpy as np
from bs4 import BeautifulSoup
from newspaper import Article
openai.api_key = st.secrets["OPENAI_API_KEY"]
SERP_API_KEY = st.secrets["SERP_API_KEY"]

def get_search_results(query, limit=10):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": limit
    }
    res = requests.get(url, params=params)
    return [r["link"] for r in res.json().get("organic_results", [])][:limit]

def scrape_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        try:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            return soup.get_text()
        except:
            return ""

def chunk_text(text, size=500):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def embed_texts(texts):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [np.array(d["embedding"]) for d in response["data"]]

def build_faiss_index(chunks):
    embeddings = embed_texts([c["text"] for c in chunks])
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

def search_faiss(index, embeddings, chunks, query):
    query_embed = embed_texts([query])[0].astype("float32")
    D, I = index.search(np.array([query_embed]), k=5)
    return [chunks[i]["text"] for i in I[0]]

def ask_gpt(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""
Based on the information below, answer the following question in a clear and concise manner. Use bullet points or numbered steps if helpful.

Question: {question}

Context:
{context}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600
    )
    return response.choices[0].message["content"].strip()

# Streamlit App
st.title("Web-powered AI Answer Assistant")

query = st.text_input("Enter your question:")
go = st.button("Search and Answer")

if go and query:
    with st.spinner("Searching and scraping..."):
        urls = get_search_results(query, limit=15)
        all_chunks = []
        for url in urls:
            text = scrape_article(url)
            if text:
                for chunk in chunk_text(text):
                    all_chunks.append({"url": url, "text": chunk})
            if len(all_chunks) >= 30:
                break

    with st.spinner("Building index..."):
        index, embeddings = build_faiss_index(all_chunks)

    with st.spinner("Getting relevant context and answering..."):
        relevant_chunks = search_faiss(index, embeddings, all_chunks, query)
        answer = ask_gpt(query, relevant_chunks)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Sources"):
        for i, c in enumerate(relevant_chunks):
            st.markdown(f"**Snippet {i+1}:**\n{c[:300]}...")

