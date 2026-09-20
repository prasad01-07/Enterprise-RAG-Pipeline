import re
import requests

from app.utils.config import LLM_MODEL


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"


# ============================================================
# FALLBACK MESSAGE
# ============================================================

REFUSAL_MESSAGE = (
    "I could not find this information in the company documents."
)


# ============================================================
# EXTRACT SOURCE NAMES
# ============================================================

def extract_source_names(context):
    """
    Extract exact SOURCE names from the context.

    Example:

    SOURCE: hr_policy.txt
    DOCUMENT CONTENT:
    ...

    Returns:

    ["hr_policy.txt"]
    """

    if not context:
        return []

    sources = []

    for line in context.splitlines():

        line = line.strip()

        if line.upper().startswith("SOURCE:"):

            source_name = line[
                len("SOURCE:"):
            ].strip()

            if source_name and source_name not in sources:
                sources.append(source_name)

    return sources


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query, context):

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not query or not query.strip():

        return "Please enter a question."

    # --------------------------------------------------------
    # Validate context
    # --------------------------------------------------------

    if not context or not context.strip():

        return REFUSAL_MESSAGE

    # --------------------------------------------------------
    # Extract exact source names
    # --------------------------------------------------------

    source_names = extract_source_names(context)

    # --------------------------------------------------------
    # Build source list for prompt
    # --------------------------------------------------------

    if source_names:

        allowed_sources = "\n".join(
            f"- {source}"
            for source in source_names
        )

    else:

        allowed_sources = "- No source name available"


    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an enterprise company knowledge assistant.

Your job is to answer the user's question using ONLY
the information provided in the DOCUMENT CONTEXT.

============================================================
STRICT RULES
============================================================

1. Use ONLY the information contained in the DOCUMENT CONTEXT.

2. Do NOT use outside knowledge.

3. Do NOT guess, assume, or invent information.

4. If the answer is not present in the DOCUMENT CONTEXT,
   respond EXACTLY with:

I could not find this information in the company documents.

5. Keep the answer short, clear, and professional.

6. At the end of the answer, provide a Sources section.

7. You MUST use ONLY the exact source names listed below.

8. NEVER invent a source name.

9. NEVER rename a source.

10. NEVER create a title such as:
    "Company Work From Home Policy"
    unless that exact text appears in the allowed source list.

11. NEVER convert a filename into a document title.

12. NEVER remove or change the filename extension.

13. If multiple retrieved documents support the answer,
    list the relevant exact source names.

14. If only one retrieved document supports the answer,
    list only that source.

15. Do NOT list a source simply because it was retrieved.
    List it only if it contains information used for the answer.

============================================================
ALLOWED SOURCE NAMES
============================================================

{allowed_sources}

============================================================
DOCUMENT CONTEXT
============================================================

{context}

============================================================
USER QUESTION
============================================================

{query}

============================================================
REQUIRED RESPONSE FORMAT
============================================================

Answer:
<short answer>

Sources:
- <exact source name from ALLOWED SOURCE NAMES>

============================================================
FINAL INSTRUCTION
============================================================

The source names in your response MUST match the
ALLOWED SOURCE NAMES character-for-character.

Do not invent, rename, summarize, or modify source names.
"""


    # ========================================================
    # CALL OLLAMA
    # ========================================================

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            ""
        ).strip()

        if not answer:

            return "The language model did not return an answer."

        # ----------------------------------------------------
        # Validate source names in generated answer
        # ----------------------------------------------------

        if source_names:

            answer_lines = answer.splitlines()

            validated_lines = []

            for line in answer_lines:

                stripped_line = line.strip()

                # --------------------------------------------
                # Check bullet source lines
                # --------------------------------------------

                if stripped_line.startswith("-"):

                    possible_source = (
                        stripped_line[1:].strip()
                    )

                    # Only treat the line as a source
                    # if it is inside the Sources section.
                    if possible_source:

                        if (
                            possible_source in source_names
                            or possible_source.startswith("📄")
                        ):

                            validated_lines.append(line)

                        else:

                            # Keep normal bullet content.
                            # We do not remove arbitrary answer bullets.
                            validated_lines.append(line)

                    else:

                        validated_lines.append(line)

                else:

                    validated_lines.append(line)

            answer = "\n".join(
                validated_lines
            ).strip()

        return answer


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to Ollama. "
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        return (
            "The request to Ollama timed out. "
            "Please try again."
        )

    except requests.exceptions.RequestException as error:

        return f"Ollama request failed: {error}"

    except Exception as error:

        return f"An unexpected error occurred: {error}"


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("Enterprise RAG Pipeline - LLM Test")
    print("=" * 70)

    test_context = """
SOURCE: hr_policy.txt
DOCUMENT CONTENT:
Employees are entitled to paid leave according to the company
HR policy. Planned leave should be submitted at least
3 working days in advance.
"""

    test_question = (
        "How many days in advance should planned leave "
        "be submitted?"
    )

    print()
    print("Question:")
    print(test_question)

    print()
    print("Generating answer...")

    answer = generate_answer(
        test_question,
        test_context
    )

    print()
    print("=" * 70)
    print("Answer")
    print("=" * 70)
    print()

    print(answer)

    print()
    print("=" * 70)