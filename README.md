# 🧠 Enterprise Document Intelligence Platform

> A production-inspired Retrieval-Augmented Generation (RAG) system that enables users to upload enterprise documents, build a searchable knowledge base, and interact with them using Large Language Models (LLMs).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-success)
![SentenceTransformers](https://img.shields.io/badge/Embeddings-BGE-green)
![Ollama](https://img.shields.io/badge/LLM-Ollama-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📌 Overview

Enterprise organizations store vast amounts of information in PDFs, Word documents, PowerPoint presentations, spreadsheets, and scanned images. Searching through these documents manually is slow and inefficient.

This project provides an AI-powered Document Intelligence Platform that:

* Uploads enterprise documents
* Extracts text using OCR when necessary
* Splits documents into semantic chunks
* Generates vector embeddings
* Stores embeddings in ChromaDB
* Retrieves the most relevant content using semantic search
* Reranks retrieved chunks with a CrossEncoder
* Uses a local LLM (Ollama) to generate grounded answers
* Displays citations for transparency

---

# ✨ Features

## 📄 Multi-format Document Support

* PDF
* DOCX
* PPTX
* XLSX
* PNG
* JPG
* JPEG

---

## 🔍 OCR Support

Automatically extracts text from scanned image documents.

---

## ✂ Intelligent Chunking

* RecursiveCharacterTextSplitter
* Configurable chunk size
* Chunk overlap
* Metadata preservation

---

## 🧠 Semantic Embeddings

Embedding Model:

**BAAI/bge-base-en-v1.5**

---

## 🗂 Vector Database

* ChromaDB
* Persistent storage
* Duplicate detection
* Document management

---

## 🔎 Retrieval Pipeline

* Semantic similarity search
* CrossEncoder reranking
* Top-K retrieval

---

## 🤖 Local LLM

Powered by:

* Ollama
* Qwen2.5:3B

No external API key required.

---

## 💬 Streamlit Interface

* Chat with documents
* Upload documents
* Document library
* Dashboard

---

# 🏗 System Architecture

```
                    Upload Document
                           │
                           ▼
                    Loader Factory
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     PDF Loader       DOCX Loader       Image Loader
                                              │
                                              ▼
                                             OCR
                           │
                           ▼
                    Document Preprocessor
                           │
                           ▼
             Recursive Character Chunker
                           │
                           ▼
                 Document Chunks
                           │
                           ▼
                 BGE Embedding Model
                           │
                           ▼
                     ChromaDB
                           │
                           ▼
                Semantic Retriever
                           │
                           ▼
              CrossEncoder Reranker
                           │
                           ▼
                  Prompt Construction
                           │
                           ▼
                    Ollama LLM
                           │
                           ▼
                 Final Answer + Sources
```

---

# 🔄 Application Workflow

## Indexing Pipeline

```
User Uploads Document
        │
        ▼
Loader Factory
        │
        ▼
Document Loader
        │
        ▼
Preprocessor
        │
        ▼
Recursive Chunker
        │
        ▼
Embedding Generator
        │
        ▼
ChromaDB
```

---

## Question Answering Pipeline

```
User Question
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB Search
      │
      ▼
Top-K Chunks
      │
      ▼
CrossEncoder Reranker
      │
      ▼
Prompt Builder
      │
      ▼
Ollama
      │
      ▼
Answer
      │
      ▼
References
```

---

# 📂 Project Structure

```
Enterprise-Document-Intelligence/
│
├── src/
│   ├── chunking/
│   ├── embeddings/
│   ├── ingestion/
│   ├── llm/
│   ├── pipeline/
│   ├── preprocessing/
│   ├── retrieval/
│   ├── services/
│   ├── vectordb/
│   └── utils/
│
├── pages/
│   ├── 1_💬_Chat.py
│   ├── 2_📂_Upload.py
│   ├── 3_📚_Library.py
│   └── 4_📊_Dashboard.py
│
├── streamlit_app/
│   └── services/
│
├── sample_documents/
│
├── vectordb/
│
├── tests/
│
├── requirements.txt
│
├── app.py
│
└── README.md
```

---

# 🛠 Tech Stack

| Category        | Technology             |
| --------------- | ---------------------- |
| Language        | Python                 |
| UI              | Streamlit              |
| OCR             | EasyOCR                |
| Embeddings      | BAAI/bge-base-en-v1.5  |
| Vector Database | ChromaDB               |
| Reranker        | BAAI/bge-reranker-base |
| LLM             | Ollama (Qwen2.5:3B)    |
| Validation      | Pydantic               |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/Enterprise-Document-Intelligence.git

cd Enterprise-Document-Intelligence
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama from:

https://ollama.com

---

## Pull the Model

```bash
ollama pull qwen2.5:3b
```

---

## Run the Application

```bash
streamlit run app.py
```

---

# 📸 Application Screenshots

![alt text](image.png)

## 💬 Chat

![alt text](image-2.png)

---

## 📂 Upload

![alt text](image-3.png)

---

## 📚 Library

![alt text](image-4.png)

---

## 📊 Dashboard

![alt text](image-5.png)

---

# 🏭 Architecture

```mermaid
flowchart TD

    %% =========================
    %% User Layer
    %% =========================
    User([👤 User])

    User --> Upload
    User --> Chat
    User --> Library
    User --> Dashboard

    %% =========================
    %% Streamlit UI
    %% =========================
    subgraph UI["🖥️ Streamlit Application"]

        Upload["📂 Upload Page"]
        Chat["💬 Chat Page"]
        Library["📚 Library"]
        Dashboard["📊 Dashboard"]

    end

    %% =========================
    %% Services
    %% =========================
    subgraph Services["⚙️ Application Services"]

        UploadService
        ChatService
        DocumentService

    end

    Upload --> UploadService
    Chat --> ChatService
    Library --> DocumentService
    Dashboard --> DocumentService

    %% =========================
    %% Indexing Pipeline
    %% =========================
    subgraph Indexing["📥 Document Indexing Pipeline"]

        LoaderFactory

        PDFLoader
        DOCXLoader
        PPTXLoader
        ExcelLoader
        ImageLoader

        OCR

        Preprocessor

        Chunker

        Embedding

        ChromaDB

    end

    UploadService --> LoaderFactory

    LoaderFactory --> PDFLoader
    LoaderFactory --> DOCXLoader
    LoaderFactory --> PPTXLoader
    LoaderFactory --> ExcelLoader
    LoaderFactory --> ImageLoader

    ImageLoader --> OCR

    PDFLoader --> Preprocessor
    DOCXLoader --> Preprocessor
    PPTXLoader --> Preprocessor
    ExcelLoader --> Preprocessor
    OCR --> Preprocessor

    Preprocessor --> Chunker

    Chunker --> Embedding

    Embedding --> ChromaDB

    %% =========================
    %% Retrieval Pipeline
    %% =========================
    subgraph Retrieval["🔍 Retrieval Pipeline"]

        QueryEmbedding

        SemanticSearch

        Reranker

    end

    %% =========================
    %% LLM
    %% =========================
    subgraph LLM["🤖 Response Generation"]

        PromptTemplate

        Ollama

        Response

    end

    ChatService --> QueryEmbedding

    QueryEmbedding --> SemanticSearch

    SemanticSearch --> ChromaDB

    ChromaDB --> SemanticSearch

    SemanticSearch --> Reranker

    Reranker --> PromptTemplate

    PromptTemplate --> Ollama

    Ollama --> Response

    Response --> Chat
```

---

# 📈 Example Queries

### Single Document

* How many annual leaves are provided?
* What is the work from home policy?
* How many medical leaves are available?

### Multiple Documents

* Compare HR Policy and Travel Policy.
* Which document mentions manager approval?
* Summarize all uploaded documents.
* Which policies discuss employee training?
* What security measures are recommended?

---

# 🔬 Future Improvements

* Hybrid Search (BM25 + Dense Retrieval)
* Metadata Filtering
* Conversation Memory
* Multi-user Authentication
* Docker Deployment
* Kubernetes Deployment
* REST API (FastAPI)
* Evaluation Dashboard
* Citation Highlighting in Documents
* Multi-language OCR
* Cloud Vector Databases

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Priyankush Biswas**

AI / Machine Learning Engineer

GitHub: https://github.com/Priyankush231

LinkedIn: https://leetcode.com/u/Priyankush08/

---

# ⭐ Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork the project
* 📝 Open issues for suggestions
* 🤝 Contribute improvements

Feedback and contributions are always welcome.
