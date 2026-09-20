# ============================================================
# Enterprise RAG Pipeline
# Main Application
# ============================================================

from app.retrieval.retriever import retrieve_documents
from app.llm.model import generate_answer


# ============================================================
# Configuration
# ============================================================

TOP_K = 3


# ============================================================
# Build Context
# ============================================================

def build_context(results):
    """
    Combine retrieved document chunks into a single
    context string for the LLM.
    """

    if not results:
        return ""

    context_parts = []

    for i, result in enumerate(results):

        source = result.get(
            "source",
            "Unknown"
        )

        text = result.get(
            "text",
            ""
        )

        context_parts.append(
            f"""
--- Document {i + 1} ---
Source: {source}

{text}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# RAG Pipeline
# ============================================================

def answer_question(query):
    """
    Complete RAG pipeline:

    1. Retrieve relevant documents
    2. Build context
    3. Send context + question to LLM
    4. Return final answer
    """

    # --------------------------------------------------------
    # Step 1 — Retrieve documents
    # --------------------------------------------------------

    print()
    print("Searching documents...")
    print()

    results = retrieve_documents(
        query,
        top_k=TOP_K
    )

    if not results:

        return (
            "I could not find relevant information "
            "in the company documents."
        ), []

    # --------------------------------------------------------
    # Step 2 — Build context
    # --------------------------------------------------------

    context = build_context(
        results
    )

    # --------------------------------------------------------
    # Step 3 — Generate answer
    # --------------------------------------------------------

    print("Generating answer...")
    print()

    answer = generate_answer(
        query,
        context
    )

    return answer, results


# ============================================================
# Display Retrieved Documents
# ============================================================

def display_results(results):

    print()
    print("=" * 70)
    print("Retrieved Documents")
    print("=" * 70)

    if not results:

        print()
        print("No relevant documents found.")
        return

    for i, result in enumerate(results):

        print()
        print(
            f"--- Retrieved Document {i + 1} ---"
        )

        print(
            f"Source: {result.get('source', 'Unknown')}"
        )

        print(
            f"Hybrid Score: "
            f"{result.get('score', 0.0):.4f}"
        )

        if "bm25_score" in result:

            print(
                f"BM25 Score: "
                f"{result['bm25_score']:.4f}"
            )

        if "semantic_score" in result:

            print(
                f"Semantic Score: "
                f"{result['semantic_score']:.4f}"
            )

        if "rrf_score" in result:

            print(
                f"RRF Score: "
                f"{result['rrf_score']:.4f}"
            )

        print()

        print(
            result.get(
                "text",
                ""
            )
        )


# ============================================================
# Main Program
# ============================================================

def main():

    print()
    print("=" * 70)
    print("Enterprise RAG Pipeline")
    print("=" * 70)

    print()
    print(
        "Ask questions about the company documents."
    )

    print(
        "Type 'exit' to quit."
    )

    print()
    print("=" * 70)

    while True:

        print()

        query = input(
            "Enter your question: "
        ).strip()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if query.lower() in {
            "exit",
            "quit"
        }:

            print()
            print(
                "Thank you for using Enterprise RAG Pipeline."
            )

            break

        # ----------------------------------------------------
        # Empty question
        # ----------------------------------------------------

        if not query:

            print(
                "Please enter a question."
            )

            continue

        # ----------------------------------------------------
        # Run RAG pipeline
        # ----------------------------------------------------

        try:

            answer, results = answer_question(
                query
            )

            # ------------------------------------------------
            # Display retrieved documents
            # ------------------------------------------------

            display_results(
                results
            )

            # ------------------------------------------------
            # Display final answer
            # ------------------------------------------------

            print()
            print("=" * 70)
            print("FINAL ANSWER")
            print("=" * 70)
            print()

            print(answer)

            print()
            print("=" * 70)

        except Exception as e:

            print()
            print("=" * 70)
            print("ERROR")
            print("=" * 70)
            print()

            print(
                f"Something went wrong: {e}"
            )

            print()


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    main()