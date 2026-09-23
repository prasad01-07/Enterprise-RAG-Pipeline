# Enterprise RAG Pipeline 🤖

An enterprise-style Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions based only on the information available in those documents.

The system combines semantic search, keyword search, hybrid retrieval, and a local Large Language Model to provide grounded answers with source citations.

---

## 🚀 Features

- 📄 Upload PDF, DOCX, and TXT documents
- ✂️ Automatic document chunking
- 🧠 Sentence Transformer embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic similarity search
- 🔤 BM25 keyword-based retrieval
- 🔀 Reciprocal Rank Fusion (RRF) hybrid retrieval
- 🤖 Local LLM using Ollama
- 📚 Source-aware answers and citations
- 🛡️ Reduces hallucinations by restricting answers to retrieved document context
- 💬 Interactive Streamlit user interface
- 🔄 Upload and index new documents directly from the UI

---

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │      User Query     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Hybrid Retrieval  │
                └──────────┬──────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │     BM25      │     │   ChromaDB    │
        │ Keyword Search│     │Semantic Search│
        └───────┬───────┘     └───────┬───────┘
                │                     │
                └──────────┬──────────┘
                           ▼
                ┌─────────────────────┐
                │  RRF Ranking        │
                │  Hybrid Results      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Retrieved Context   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Ollama LLM          │
                │ Llama 3.2           │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Grounded Answer     │
                │ + Source Citations  │
                └─────────────────────┘

               ## 📂 Project Structure

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


      ##🛠️ Technologies Used
Technology
Purpose
Python
Core programming language
Streamlit
Web user interface
Sentence Transformers
Text embeddings
ChromaDB
Vector database
BM25
Keyword retrieval
RRF
Hybrid result ranking
Ollama
Local LLM inference
Llama 3.2
Language model
PyPDF
PDF document extraction
python-docx
DOCX document extraction

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core programming language |
| Streamlit | Web user interface |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| BM25 | Keyword retrieval |
| RRF | Hybrid result ranking |
| Ollama | Local LLM inference |
| Llama 3.2 | Language model |
| PyPDF | PDF document extraction |
| python-docx | DOCX document extraction |

🔄 RAG Pipeline

The system follows these major stages:
1. Document Ingestion
Users can upload:
PDF
DOCX
TXT
The system extracts the text from the uploaded document.
2. Text Chunking
Large documents are divided into smaller overlapping chunks so that relevant information can be retrieved efficiently.
3. Embeddings
Each chunk is converted into a numerical vector using a Sentence Transformer embedding model.
4. Vector Storage
The generated embeddings are stored in ChromaDB.
5. Keyword Retrieval
BM25 searches the document collection using keyword-based matching.
6. Semantic Retrieval
ChromaDB performs semantic similarity search using vector embeddings.
7. Hybrid Retrieval
BM25 and semantic results are combined using Reciprocal Rank Fusion (RRF).
8. Context Generation
The highest-ranked document chunks are provided as context to the LLM.
9. Answer Generation
Ollama runs the local Llama 3.2 model to generate an answer based on the retrieved context.
10. Source Citation
The application displays the document sources used to generate the answer.

🛡️ Hallucination Protection

The system is designed to answer questions using only the retrieved document context.
If the required information cannot be found in the available documents, the system responds:
I could not find this information in the company documents.
This helps prevent the model from generating unsupported information.

💻 Running the Project

1. Clone the repository
git clone https://github.com/prasad01-07/Enterprise-RAG-Pipeline.git

2. Open the project
cd Enterprise-RAG-Pipeline

3. Create a virtual environment
python -m venv venv

4. Activate the virtual environment on Windows
venv\Scripts\activate

5. Install dependencies
pip install -r requirements.txt

6. Install and run Ollama
Install Ollama and make sure the required model is available:
ollama pull llama3.2
Start Ollama if required:
ollama serve

7. Run the Streamlit application
streamlit run app/ui.py
The application will open in the browser.

📚 Supported Documents
Currently supported:
.pdf
.docx
.txt
Users can upload documents directly through the Streamlit interface.

🧪 Example Questions

The system has been tested with real-world and policy documents.
Example:

What was 3M's net sales in 2021?
The system retrieves the relevant information from the 3M annual report and provides the answer with its source.
Other examples:
How many days can employees work from home?

How many vacation days do employees receive?

How many days in advance should planned leave be submitted?

🎯 Project Goals

The main goals of this project are:
Build a practical RAG pipeline
Improve retrieval quality using hybrid search
Reduce LLM hallucinations
Provide source-grounded answers
Support multiple document formats
Build an enterprise-style document question-answering system

🔮 Future Improvements

Relevance threshold filtering
Conversation memory
Better document metadata
Advanced reranking
Multi-modal document support
Authentication and user management
Docker deployment
Cloud deployment
REST API improvements
Production monitoring

## 🔗 Project Links

- 📂 **GitHub Repository:** [Enterprise RAG Pipeline](https://github.com/prasad01-07/Enterprise-RAG-Pipeline)
- 🌐 **Live Demo:** coming soong

## 👨‍💻 About the Author

**J Prasad**

🎓 B.Tech in Computer Science & Engineering – Artificial Intelligence & Machine Learning  
🏫 Sri Indu Institute of Engineering and Technology  
💡 Interested in Artificial Intelligence, Machine Learning, LLMs, RAG Systems and Generative AI  
🚀 Currently building practical AI/ML projects and improving software development skills

⭐ If you find this project useful, feel free to explore the repository.