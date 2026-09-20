from pathlib import Path
import re

from rank_bm25 import BM25Okapi

from app.retrieval.vector_store import collection, embedding_model


# ============================================================
# CONFIGURATION
# ============================================================

RRF_K = 60

BM25_WEIGHT = 0.5
SEMANTIC_WEIGHT = 0.5

# Minimum semantic similarity required for a document
# to be considered relevant.
MIN_SEMANTIC_SIMILARITY = 0.35


# ============================================================
# SOURCE NAME CLEANING
# ============================================================

def clean_source_name(source):
    """
    Convert a full document path into a clean filename.
    """

    if not source:
        return "Unknown source"

    return Path(source).name


# ============================================================
# TEXT TOKENIZATION
# ============================================================

def tokenize(text):
    """
    Simple tokenizer for BM25.
    """

    return re.findall(r"\b\w+\b", text.lower())


# ============================================================
# BM25 SEARCH
# ============================================================

def bm25_search(query, documents, top_k):
    """
    Perform keyword-based BM25 retrieval.
    """

    if not documents:
        return []

    tokenized_documents = [
        tokenize(document["text"])
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )

    results = []

    for index in ranked_indices[:top_k]:

        results.append({
            "text": documents[index]["text"],
            "source": documents[index]["source"],
            "bm25_score": float(scores[index]),
        })

    return results


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(query, top_k):
    """
    Perform semantic search using ChromaDB.
    """

    total_documents = collection.count()

    if total_documents == 0:
        return []

    query_embedding = embedding_model.encode(query).tolist()

    result_count = min(
        total_documents,
        max(top_k * 5, 15)
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=result_count,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    semantic_results = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for index, text in enumerate(documents):

        source = (
            metadatas[index].get("source", "Unknown source")
            if index < len(metadatas)
            else "Unknown source"
        )

        distance = (
            float(distances[index])
            if index < len(distances)
            else 1.0
        )

        # Chroma cosine distance:
        # similarity = 1 - distance
        semantic_similarity = max(
            0.0,
            1.0 - distance
        )

        semantic_results.append({
            "text": text,
            "source": source,
            "semantic_score": semantic_similarity,
        })

    return semantic_results


# ============================================================
# RECIPROCAL RANK FUSION
# ============================================================

def rrf_score(rank, weight):
    """
    Calculate weighted Reciprocal Rank Fusion score.
    """

    return weight / (RRF_K + rank)


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

def retrieve_documents(query, top_k=3):
    """
    Hybrid retrieval using:

    1. BM25 keyword search
    2. Semantic search
    3. Reciprocal Rank Fusion
    4. Semantic relevance filtering

    Returns the most relevant document chunks.
    """

    if not query or not query.strip():
        return []

    query = query.strip()

    # --------------------------------------------------------
    # Get all documents from ChromaDB
    # --------------------------------------------------------

    stored_documents = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = stored_documents.get("documents", [])
    metadatas = stored_documents.get("metadatas", [])

    if not documents:
        return []

    all_documents = []

    for index, text in enumerate(documents):

        source = (
            metadatas[index].get("source", "Unknown source")
            if index < len(metadatas)
            else "Unknown source"
        )

        all_documents.append({
            "text": text,
            "source": source,
        })

    # --------------------------------------------------------
    # BM25 retrieval
    # --------------------------------------------------------

    bm25_results = bm25_search(
        query,
        all_documents,
        top_k=max(top_k * 5, 15)
    )

    # --------------------------------------------------------
    # Semantic retrieval
    # --------------------------------------------------------

    semantic_results = semantic_search(
        query,
        top_k=max(top_k * 5, 15)
    )

    # --------------------------------------------------------
    # Create lookup tables
    # --------------------------------------------------------

    bm25_lookup = {}

    for rank, result in enumerate(bm25_results, start=1):

        key = (
            result["source"],
            result["text"]
        )

        bm25_lookup[key] = {
            "rank": rank,
            "score": result["bm25_score"]
        }

    semantic_lookup = {}

    for rank, result in enumerate(
        semantic_results,
        start=1
    ):

        key = (
            result["source"],
            result["text"]
        )

        semantic_lookup[key] = {
            "rank": rank,
            "score": result["semantic_score"]
        }

    # --------------------------------------------------------
    # RRF FUSION
    # --------------------------------------------------------

    candidate_keys = set(
        bm25_lookup.keys()
    ).union(
        semantic_lookup.keys()
    )

    fused_results = []

    for key in candidate_keys:

        source, text = key

        bm25_data = bm25_lookup.get(key)

        semantic_data = semantic_lookup.get(key)

        bm25_score = (
            bm25_data["score"]
            if bm25_data
            else 0.0
        )

        semantic_score = (
            semantic_data["score"]
            if semantic_data
            else 0.0
        )

        bm25_rank = (
            bm25_data["rank"]
            if bm25_data
            else None
        )

        semantic_rank = (
            semantic_data["rank"]
            if semantic_data
            else None
        )

        rrf_score_value = 0.0

        if bm25_rank is not None:
            rrf_score_value += rrf_score(
                bm25_rank,
                BM25_WEIGHT
            )

        if semantic_rank is not None:
            rrf_score_value += rrf_score(
                semantic_rank,
                SEMANTIC_WEIGHT
            )

        fused_results.append({
            "text": text,
            "source": source,
            "source_name": clean_source_name(source),
            "score": rrf_score_value,
            "bm25_score": bm25_score,
            "semantic_score": semantic_score,
        })

    # --------------------------------------------------------
    # SORT BY RRF SCORE
    # --------------------------------------------------------

    fused_results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # SEMANTIC RELEVANCE FILTER
    # --------------------------------------------------------

    # Find the strongest semantic match.
    semantic_scores = [
        result["semantic_score"]
        for result in fused_results
        if result["semantic_score"] > 0
    ]

    if semantic_scores:

        best_semantic_score = max(
            semantic_scores
        )

        # Dynamic threshold:
        # keep documents reasonably close to
        # the strongest semantic match.
        dynamic_threshold = max(
            MIN_SEMANTIC_SIMILARITY,
            best_semantic_score * 0.72
        )

        filtered_results = [
            result
            for result in fused_results
            if result["semantic_score"]
            >= dynamic_threshold
        ]

    else:

        filtered_results = fused_results

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    # If filtering removed everything,
    # return the strongest result rather than nothing.
    if not filtered_results and fused_results:
        filtered_results = [
            fused_results[0]
        ]

    # --------------------------------------------------------
    # FINAL TOP-K RESULTS
    # --------------------------------------------------------

    final_results = filtered_results[:top_k]

    return final_results


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_questions = [
        "What types of leave can employees take?",
        "How many vacation days do employees receive?",
        "What is the work from home policy?",
        "What was 3M's net sales in 2021?",
        "What is the CEO's favorite food?",
        "How many days in advance should planned leave be submitted?",
    ]

    print("\n")
    print("=" * 80)
    print("HYBRID RAG RETRIEVAL TEST")
    print("=" * 80)

    for question in test_questions:

        print("\n")
        print("-" * 80)
        print("QUESTION:")
        print(question)
        print("-" * 80)

        results = retrieve_documents(
            question,
            top_k=3
        )

        if not results:

            print("No relevant documents found.")

            continue

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{index}. "
                f"{result['source_name']}"
            )

            print(
                f"   RRF Score: "
                f"{result['score']:.5f}"
            )

            print(
                f"   BM25 Score: "
                f"{result['bm25_score']:.5f}"
            )

            print(
                f"   Semantic Score: "
                f"{result['semantic_score']:.5f}"
            )

            print(
                f"   Text: "
                f"{result['text'][:180]}..."
            )

    print("\n")
    print("=" * 80)
    print("RETRIEVAL TEST COMPLETE")
    print("=" * 80)