def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    Split documents into smaller chunks.
    """

    chunks = []

    for document in documents:
        text = document["text"]
        source = document["source"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "source": source
            })

            start = end - chunk_overlap

    return chunks