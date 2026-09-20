
from pathlib import Path

from app.utils.config import DOCUMENTS_DIR
from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import add_documents


# ============================================================
# Supported File Types
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


# ============================================================
# Save Uploaded File
# ============================================================

def save_uploaded_file(uploaded_file):
    """
    Save a Streamlit uploaded file
    into the documents directory.
    """

    if uploaded_file is None:
        raise ValueError("No file was provided.")

    filename = Path(uploaded_file.name).name
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: TXT, PDF, DOCX."
        )

    documents_dir = Path(DOCUMENTS_DIR)

    documents_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = documents_dir / filename

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


# ============================================================
# Index Uploaded File
# ============================================================

def index_uploaded_file(uploaded_file):
    """
    Save, load, chunk and index one uploaded document.
    """

    # --------------------------------------------------------
    # Step 1 — Save file
    # --------------------------------------------------------

    file_path = save_uploaded_file(
        uploaded_file
    )

    print(
        f"Saved uploaded file: {file_path}"
    )

    # --------------------------------------------------------
    # Step 2 — Load document
    # --------------------------------------------------------

    document = load_document(
        file_path
    )

    if not document["text"]:
        raise ValueError(
            "No text could be extracted from the document."
        )

    print(
        f"Extracted {len(document['text'])} characters."
    )

    # --------------------------------------------------------
    # Step 3 — Create chunks
    # --------------------------------------------------------

    chunks = chunk_documents(
        [document]
    )

    if not chunks:
        raise ValueError(
            "No chunks were created."
        )

    print(
        f"Created {len(chunks)} chunks."
    )

    # --------------------------------------------------------
    # Step 4 — Store in ChromaDB
    # --------------------------------------------------------

    add_documents(
        chunks
    )

    print(
        "Document successfully indexed."
    )

    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "characters": len(document["text"]),
        "chunks": len(chunks)
    }


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("Upload Module")
    print("=" * 70)
    print()
    print("Upload module is ready.")
    print()