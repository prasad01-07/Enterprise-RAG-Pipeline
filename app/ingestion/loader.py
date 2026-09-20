from pathlib import Path

from pypdf import PdfReader
from docx import Document

from app.utils.config import DOCUMENTS_DIR


# ============================================================
# Supported File Types
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


# ============================================================
# Load TXT File
# ============================================================

def load_txt(file_path):
    """
    Load text from a TXT file.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()

    return text.strip()


# ============================================================
# Load PDF File
# ============================================================

def load_pdf(file_path):
    """
    Extract text from all pages of a PDF file.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages).strip()


# ============================================================
# Load DOCX File
# ============================================================

def load_docx(file_path):
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs).strip()


# ============================================================
# Load Single Document
# ============================================================

def load_document(file_path):
    """
    Load one document based on its file extension.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()


    if extension == ".txt":

        text = load_txt(file_path)


    elif extension == ".pdf":

        text = load_pdf(file_path)


    elif extension == ".docx":

        text = load_docx(file_path)


    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )


    if not text:

        print(
            f"Warning: No text extracted from {file_path.name}"
        )


    return {
        "text": text,
        "source": str(file_path)
    }


# ============================================================
# Load All Documents
# ============================================================

def load_documents(directory=DOCUMENTS_DIR):
    """
    Load all supported documents from a directory.

    Supported:
        TXT
        PDF
        DOCX
    """

    directory = Path(directory)

    documents = []


    if not directory.exists():

        print(
            f"Document directory does not exist: {directory}"
        )

        return documents


    print()
    print("=" * 70)
    print("Loading Documents")
    print("=" * 70)


    for file_path in sorted(
        directory.iterdir()
    ):

        if not file_path.is_file():

            continue


        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:

            continue


        try:

            document = load_document(
                file_path
            )


            if document["text"]:

                documents.append(
                    document
                )


                print(
                    f"Loaded: {file_path.name}"
                )


        except Exception as error:

            print(
                f"Failed to load {file_path.name}: {error}"
            )


    print()
    print(
        f"Total documents loaded: {len(documents)}"
    )

    print("=" * 70)


    return documents


# ============================================================
# Test Loader
# ============================================================

if __name__ == "__main__":

    documents = load_documents()


    print()
    print("=" * 70)
    print("Document Loader Test")
    print("=" * 70)


    if not documents:

        print(
            "No documents found."
        )


    else:

        for i, document in enumerate(
            documents,
            start=1
        ):

            print()
            print(
                f"--- Document {i} ---"
            )


            print(
                f"Source: {document['source']}"
            )


            print(
                f"Characters: {len(document['text'])}"
            )


            print()
            print(
                document["text"][:500]
            )


    print()
    print("=" * 70)