# 🚀 StarMind RAG

> **A modern, privacy-first Retrieval-Augmented Generation (RAG) platform for intelligent document analysis and conversational AI.**

StarMind RAG is a local-first knowledge engine that transforms your documents into a searchable semantic database. It combines vector search, AI-powered reasoning, and an intuitive cyberpunk-inspired interface to provide fast, accurate, and explainable answers from your own knowledge base.

Unlike traditional keyword search, StarMind understands the semantic meaning of your documents and retrieves the most relevant information before generating a response.

---

# ✨ Features

- 🔒 **Privacy First**
  - All documents remain on your machine.
  - No cloud storage required.
  - Local vector database.

- 🧠 **Semantic Search**
  - Embedding-based document retrieval.
  - Context-aware responses.
  - Intelligent chunk ranking.

- 📄 **Multi-Document Support**
  - PDF
  - DOCX
  - TXT
  - Markdown

- ⚡ **Hybrid Retrieval**
  - Local knowledge base
  - Optional web search
  - Combined contextual responses

- 💬 **Conversational AI**
  - Context-aware chat
  - Conversation history
  - Markdown responses

- 🎨 **Modern Dashboard**
  - Glassmorphism UI
  - Animated Quantum Core
  - Interactive knowledge cards
  - Responsive layout

---

# 🏗 Architecture

```text
                     User
                       │
                       ▼
                 FastAPI Backend
                       │
        ┌──────────────┼──────────────┐
        ▼                             ▼
   Vector Database              Optional Web Search
      (ChromaDB)                 (DuckDuckGo)
        │                             │
        └──────────────┬──────────────┘
                       ▼
                 Context Builder
                       │
                       ▼
                 Language Model
             (Groq / Ollama / OpenAI)
                       │
                       ▼
                  Final Response
```

---

# 🧠 How Retrieval Works

```text
Documents

↓

Chunking

↓

Embeddings

↓

ChromaDB

↓

User Question

↓

Question Embedding

↓

Similarity Search

↓

Top Relevant Chunks

↓

LLM

↓

AI Response
```

---

# 🛠 Tech Stack

### Backend

- Python 3.10+
- FastAPI
- Uvicorn

### AI

- SentenceTransformers
- ChromaDB
- Groq API *(default)*
- Ollama *(optional)*
- OpenAI *(optional)*

### Frontend

- HTML5
- CSS3
- JavaScript (ES6)
- Marked.js

---

# 📂 Project Structure

```text
StarMind-RAG/

├── app/
│   ├── main.py
│   ├── api/
│   ├── rag/
│   └── llm/
│
├── data/
│   ├── documents/
│   └── chroma/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── scripts/
│   └── index_documents.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/StarMind-RAG.git

cd StarMind-RAG
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# 📚 Build Your Knowledge Base

Place your documents inside:

```text
data/documents/
```

Supported formats:

- PDF
- DOCX
- TXT
- Markdown

Then index them.

```bash
python scripts/index_documents.py
```

This process:

- extracts text
- splits documents into chunks
- generates embeddings
- stores vectors in ChromaDB

---

# ▶ Running

Start the API.

```bash
python app/main.py
```

or

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

# 🌐 API

## System Status

```
GET /api/system-status
```

Returns:

- system information
- status
- dashboard tips

---

## Semantic Search

```
POST /api/search
```

Performs:

- embedding generation
- vector similarity search
- context retrieval
- AI response generation

---

## Chat

```
POST /api/chat
```

Maintains short-term conversation history while leveraging the document knowledge base.

---

# 🔍 Retrieval Pipeline

```text
User Question

↓

Embedding Model

↓

Vector Search

↓

Top-K Chunks

↓

Prompt Builder

↓

Language Model

↓

Answer + Sources
```

---

# 🔐 Privacy

StarMind is designed with a local-first philosophy.

Your documents remain under your control.

The vector database is stored locally.

No document content is uploaded to external services unless you explicitly configure an online language model.

---

# 📈 Roadmap

- [ ] PDF support
- [ ] DOCX support
- [ ] Markdown support
- [ ] Image OCR
- [ ] Audio transcription
- [ ] Video transcript indexing
- [ ] Hybrid Retrieval
- [ ] Multi-user workspaces
- [ ] Plugin system
- [ ] Knowledge Graph
- [ ] Agentic Retrieval
- [ ] Streaming responses

---

# 📜 License

MIT License

---

# ⭐ StarMind

**Think beyond search. Retrieve knowledge. Generate intelligence.**
