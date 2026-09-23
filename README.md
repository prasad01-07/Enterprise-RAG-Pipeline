# Enterprise RAG Pipeline 🤖

An enterprise-style **Retrieval-Augmented Generation (RAG)** system that allows users to upload documents and ask questions based only on the information available in those documents.

The system combines **semantic search, keyword search, hybrid retrieval, Reciprocal Rank Fusion (RRF), and a local Large Language Model** to provide grounded answers with source citations.

---

## 🚀 Live Demo

🌐 **Live Demo:** Coming soon

The application currently runs locally using **Streamlit** and **Ollama**.

---

## 📁 GitHub Repository

🔗 **Repository:** [Enterprise RAG Pipeline](https://github.com/prasad01-07/Enterprise-RAG-Pipeline)

---

## ✨ Features

- 📄 Upload PDF, DOCX, and TXT documents
- ✂️ Automatic document chunking
- 🧠 Sentence Transformer embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic similarity search
- 🔤 BM25 keyword-based retrieval
- 🔀 Reciprocal Rank Fusion (RRF) hybrid retrieval
- 🤖 Local LLM using Ollama
- 🦙 Llama 3.2 language model
- 📚 Source-aware answers and citations
- 🛡️ Hallucination protection
- 💻 Interactive Streamlit user interface
- 📤 Upload and index new documents directly from the UI
- 🔍 Document-based question answering

---

## 🏗️ Architecture

The system follows a retrieval-augmented generation architecture:

```text
                    User Query
                        │
                        ▼
              ┌──────────────────┐
              │  Query Processing │
              └────────┬─────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      ┌─────────────┐     ┌─────────────┐
      │ BM25 Search │     │   Semantic  │
      │   Keyword   │     │    Search   │
      └──────┬──────┘     └──────┬──────┘
             │                   │
             └─────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │  RRF Hybrid      │
              │    Retrieval     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Retrieved Context│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Ollama LLM     │
              │    Llama 3.2     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Grounded Answer  │
              │ + Source Citation│
              └──────────────────┘
```

---

## 📂 Project Structure

```text
Enterprise-RAG-Pipeline/
│
├── app/
│   ├── api/
│   │   └── main.py
│   │
│   ├── ingestion/
│   │   ├── chunker.py
│   │   ├── loader.py
│   │   └── upload.py
│   │
│   ├── llm/
│   │   └── model.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── utils/
│   │   └── config.py
│   │
│   ├── main.py
│   └── ui.py
│
├── data/
│   └── documents/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.12** — Core programming language
- **Streamlit** — Interactive web user interface
- **Sentence Transformers** — Text embeddings
- **ChromaDB** — Vector database
- **BM25** — Keyword-based retrieval
- **RRF** — Hybrid result ranking
- **Ollama** — Local LLM inference
- **Llama 3.2** — Language model
- **PyPDF** — PDF document extraction
- **python-docx** — DOCX document extraction
- **LangChain concepts** — RAG and LLM workflow

---

## 🔄 RAG Pipeline

The system follows these major stages:

### 1. 📄 Document Ingestion

Users can upload:

- PDF
- DOCX
- TXT

The system extracts the text from the uploaded document.

### 2. ✂️ Text Chunking

Large documents are divided into smaller overlapping chunks so that relevant information can be retrieved efficiently.

The current configuration uses:

```text
Chunk Size: 500 characters
Chunk Overlap: 50 characters
```

### 3. 🧠 Embeddings

Each document chunk is converted into a numerical vector using a **Sentence Transformer embedding model**.

### 4. 🗄️ Vector Storage

The generated embeddings are stored in **ChromaDB** for semantic retrieval.

### 5. 🔤 Keyword Retrieval

**BM25** searches the document collection using keyword-based matching.

This helps retrieve information when important terms appear directly in the query.

### 6. 🔎 Semantic Retrieval

ChromaDB performs semantic similarity search using vector embeddings.

This allows the system to retrieve information based on meaning rather than only exact keywords.

### 7. 🔀 Hybrid Retrieval

BM25 and semantic search results are combined using **Reciprocal Rank Fusion (RRF)**.

This provides a hybrid retrieval approach that uses both:

- Keyword relevance
- Semantic relevance

### 8. 📚 Context Generation

The highest-ranked document chunks are selected and provided as context to the LLM.

### 9. 🤖 Answer Generation

Ollama runs the local **Llama 3.2** model to generate an answer based on the retrieved document context.

### 10. 📌 Source Citation

The application displays the document sources used to generate the answer.

---

## 🛡️ Hallucination Protection

The system is designed to answer questions using **only the retrieved document context**.

If the required information cannot be found in the available documents, the system responds:

```text
I could not find this information in the company documents.
```

This helps prevent the model from generating unsupported information outside the retrieved document context.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prasad01-07/Enterprise-RAG-Pipeline.git
cd Enterprise-RAG-Pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install and Run Ollama

Install Ollama on your system and make sure the required model is available.

Pull Llama 3.2:

```bash
ollama pull llama3.2
```

If Ollama is not already running:

```bash
ollama serve
```

### 6. Run the Streamlit Application

```bash
streamlit run app/ui.py
```

The application will open in your browser.

---

## 📄 Supported Documents

The application currently supports:

- `.pdf`
- `.docx`
- `.txt`

Users can upload documents directly through the Streamlit interface.

---

## 🧪 Example Questions

The system has been tested with real-world and policy documents.

### Example 1

**Question:**

```text
What was 3M's net sales in 2021?
```

The system retrieves the relevant information from the 3M annual report and generates an answer with the document source.

### Example 2

```text
How many days can employees work from home?
```

### Example 3

```text
How many vacation days do employees receive?
```

### Example 4

```text
How many days in advance should planned leave be submitted?
```

### Example 5

```text
What types of leave can employees take?
```

The system can also refuse to answer when the requested information is not available in the indexed documents.

---

## 🎯 Project Goals

The main goals of this project are:

- Build a practical RAG pipeline
- Improve retrieval quality using hybrid search
- Combine keyword and semantic retrieval
- Reduce unsupported LLM responses
- Provide source-grounded answers
- Support multiple document formats
- Build an enterprise-style document question-answering system
- Understand the complete RAG workflow from ingestion to generation

---

## 📊 Project Highlights

- 🔎 Hybrid BM25 + semantic retrieval
- 🔀 Reciprocal Rank Fusion
- 🧠 Sentence Transformer embeddings
- 🗄️ ChromaDB vector storage
- 🤖 Local Llama 3.2 inference
- 📚 Source-grounded responses
- 🛡️ Context-based hallucination protection
- 📄 PDF, DOCX, and TXT support
- 💻 Interactive Streamlit interface
- 📤 Direct document upload and indexing

---

## 🔮 Future Improvements

Planned improvements include:

- Relevance threshold filtering
- Conversation memory
- Better document metadata
- Advanced reranking
- Multi-modal document support
- Authentication and user management
- Docker deployment
- Cloud deployment
- REST API improvements
- Production monitoring

---

## 👨‍💻 About the Author

**J Prasad**

🎓 B.Tech in Computer Science & Engineering – Artificial Intelligence & Machine Learning

🏫 Sri Indu Institute of Engineering and Technology

💡 Interested in Artificial Intelligence, Machine Learning, LLMs, RAG Systems and Generative AI

🚀 Currently building practical AI/ML projects and improving software development skills

---

## ⭐ Project

If you find this project useful, feel free to explore the repository.

🔗 [Enterprise RAG Pipeline on GitHub](https://github.com/prasad01-07/Enterprise-RAG-Pipeline)