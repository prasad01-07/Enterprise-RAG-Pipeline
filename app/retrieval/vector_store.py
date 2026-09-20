import hashlib
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.utils.config import EMBEDDING_MODEL, CHROMA_DB_DIR


# ============================================================
# 1. Load Embedding Model
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# ============================================================
# 2. Create ChromaDB Client
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_DB_DIR
)


# ============================================================
# 3. Create or Get Collection
# ============================================================

collection = client.get_or_create_collection(
    name="documents"
)


# ============================================================
# 4. Normalize Source Path
# ============================================================

def normalize_source(source):
    """
    Convert different representations of the same file
    into one consistent source path.
    """

    return str(
        Path(source).resolve()
    ).lower()


# ============================================================
# 5. Generate Stable Document ID
# ============================================================

def generate_document_id(source, text):
    """
    Generate a stable unique ID using normalized source + text.
    """

    normalized_source = normalize_source(
        source
    )

    content = (
        f"{normalized_source}:{text}"
    )

    return hashlib.md5(
        content.encode("utf-8")
    ).hexdigest()


# ============================================================
# 6. Add Documents
# ============================================================

def add_documents(chunks):
    """
    Add document chunks and embeddings to ChromaDB.
    """

    if not chunks:

        print("No chunks found.")

        return


    texts = [
        chunk["text"]
        for chunk in chunks
    ]


    sources = [
        normalize_source(
            chunk["source"]
        )
        for chunk in chunks
    ]


    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    embeddings = embedding_model.encode(
        texts
    ).tolist()


    # --------------------------------------------------------
    # Create stable IDs
    # --------------------------------------------------------

    ids = [
        generate_document_id(
            source,
            text
        )
        for source, text in zip(
            sources,
            texts
        )
    ]


    # --------------------------------------------------------
    # Create metadata
    # --------------------------------------------------------

    metadatas = [
        {
            "source": source
        }
        for source in sources
    ]


    # --------------------------------------------------------
    # Store in ChromaDB
    # --------------------------------------------------------

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )


    print(
        f"Added/updated {len(texts)} chunks in ChromaDB."
    )


# ============================================================
# 7. Reset Collection
# ============================================================

def reset_collection():
    """
    Delete the existing collection and create a fresh one.

    Used once to remove old duplicate records.
    """

    global collection

    try:

        client.delete_collection(
            name="documents"
        )

        print(
            "Existing ChromaDB collection deleted."
        )

    except Exception:

        print(
            "No existing collection to delete."
        )


    collection = client.get_or_create_collection(
        name="documents"
    )

    print(
        "Fresh ChromaDB collection created."
    )


# ============================================================
# 8. Display Collection Information
# ============================================================

def get_collection_count():

    return collection.count()


# ============================================================
# 9. Run Ingestion
# ============================================================

if __name__ == "__main__":

    from app.ingestion.loader import load_documents
    from app.ingestion.chunker import chunk_documents


    print()
    print("=" * 70)
    print("Enterprise RAG Pipeline - Vector Store")
    print("=" * 70)


    # --------------------------------------------------------
    # Load documents
    # --------------------------------------------------------

    docs = load_documents(
        "data/documents"
    )

    print(
        f"Loaded documents: {len(docs)}"
    )


    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = chunk_documents(
        docs
    )

    print(
        f"Created chunks: {len(chunks)}"
    )


    # --------------------------------------------------------
    # Add documents
    # --------------------------------------------------------

    add_documents(
        chunks
    )


    print()
    print(
        f"ChromaDB total chunks: "
        f"{get_collection_count()}"
    )


    print()
    print("=" * 70)