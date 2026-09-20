from pathlib import Path
import sys
import textwrap
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from app.retrieval.retriever import retrieve_documents
from app.llm.model import generate_answer
from app.ingestion.upload import index_uploaded_file


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = []

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_source_name(source):

    if not source:
        return "Unknown source"

    return Path(str(source)).name


def get_unique_sources(results):

    sources = []

    for result in results:

        source_name = result.get("source_name")

        if not source_name:
            source_name = clean_source_name(
                result.get("source", "")
            )

        if source_name and source_name not in sources:
            sources.append(source_name)

    return sources


def build_context(results):

    context_parts = []

    for index, result in enumerate(results, start=1):

        source_name = result.get("source_name")

        if not source_name:
            source_name = clean_source_name(
                result.get("source", "")
            )

        text = result.get("text", "")

        context_parts.append(
            f"SOURCE {index}: {source_name}\n\n"
            f"DOCUMENT CONTENT:\n{text}\n"
        )

    return "\n".join(context_parts)


def clear_question():

    st.session_state.question_input = ""
    st.session_state.results = []
    st.session_state.answer = ""
    st.session_state.sources = []
    st.session_state.last_question = ""


def set_example_question(question):

    st.session_state.question_input = question


def process_question(question, top_k):

    question = question.strip()

    if not question:

        st.warning(
            "Please enter a question."
        )

        return

    with st.spinner(
        "Searching enterprise knowledge..."
    ):

        results = retrieve_documents(
            question,
            top_k=top_k
        )

        st.session_state.results = results

        if not results:

            st.session_state.answer = (
                "I could not find this information "
                "in the company documents."
            )

            st.session_state.sources = []
            st.session_state.last_question = question

            return

        context = build_context(results)

        answer = generate_answer(
            question,
            context
        )

        st.session_state.answer = answer

        st.session_state.sources = (
            get_unique_sources(results)
        )

        st.session_state.last_question = question


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):

    st.html(
        textwrap.dedent(content)
    )


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
"""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(108, 72, 255, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 5% 85%,
            rgba(0, 198, 255, 0.12),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #030510 0%,
            #070b1c 45%,
            #03040c 100%
        );

    color: #f4f7ff;
}


header {
    background: transparent !important;
}


.block-container {

    max-width: 1500px;

    padding-top: 2rem;
    padding-bottom: 4rem;

}


[data-testid="stAppViewContainer"] {
    background: transparent;
}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050713;
}

::-webkit-scrollbar-thumb {

    background:
        linear-gradient(
            180deg,
            #6148ff,
            #159eea
        );

    border-radius: 20px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(7, 11, 31, 0.98),
            rgba(3, 6, 18, 0.98)
        ) !important;

    border-right:
        1px solid
        rgba(115, 95, 255, 0.20);

    box-shadow:
        10px 0 50px
        rgba(0, 0, 0, 0.30);
}


.sidebar-logo {

    text-align: center;

    padding:
        18px
        5px
        24px
        5px;

}


.sidebar-logo-icon {

    width: 76px;
    height: 76px;

    margin: auto;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 23px;

    font-size: 38px;

    background:
        linear-gradient(
            135deg,
            #35219d,
            #1457a8
        );

    border:
        1px solid
        rgba(150, 130, 255, 0.55);

    box-shadow:
        0 0 30px
        rgba(83, 64, 255, 0.35),

        inset 0 0 25px
        rgba(100, 80, 255, 0.25);

    animation:
        logoPulse 4s ease-in-out infinite;

}


@keyframes logoPulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.04);
    }

}


.sidebar-title {

    margin-top: 14px;

    font-size: 21px;

    font-weight: 850;

    letter-spacing: -0.5px;

}


.sidebar-subtitle {

    margin-top: 5px;

    color: #7781a5;

    font-size: 12px;

}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    position: relative;

    overflow: hidden;

    min-height: 350px;

    padding: 45px;

    border-radius: 32px;

    background:

        radial-gradient(
            circle at 88% 50%,
            rgba(105, 60, 255, 0.32),
            transparent 36%
        ),

        linear-gradient(
            135deg,
            rgba(21, 27, 67, 0.95),
            rgba(6, 10, 28, 0.97)
        );

    border:
        1px solid
        rgba(121, 102, 255, 0.30);

    box-shadow:

        0 30px 90px
        rgba(0, 0, 0, 0.40),

        inset 0 1px
        rgba(255,255,255,0.08);

}


.hero-badge {

    display: inline-flex;

    align-items: center;

    gap: 9px;

    padding:
        8px 14px;

    border-radius: 50px;

    color: #62e7ad;

    font-size: 11px;

    font-weight: 800;

    background:
        rgba(46, 220, 151, 0.07);

    border:
        1px solid
        rgba(67, 227, 162, 0.25);

}


.online-dot {

    width: 8px;
    height: 8px;

    display: inline-block;

    border-radius: 50%;

    background: #42e6a3;

    box-shadow:
        0 0 7px #42e6a3,
        0 0 16px rgba(66,230,163,0.55);

    animation:
        onlinePulse 2s infinite;

}


@keyframes onlinePulse {

    0% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: 0.55;
        transform: scale(0.75);
    }

    100% {
        opacity: 1;
        transform: scale(1);
    }

}


.hero-title {

    margin-top: 24px;

    font-size:
        clamp(
            40px,
            5vw,
            66px
        );

    line-height: 1.02;

    font-weight: 900;

    letter-spacing: -2.8px;

}


.gradient-text {

    background:
        linear-gradient(
            90deg,
            #ffffff 5%,
            #9a82ff 45%,
            #40cfff 100%
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color:
        transparent;

}


.hero-description {

    max-width: 720px;

    margin-top: 20px;

    color: #9ba5c7;

    font-size: 15px;

    line-height: 1.75;

}


/* ============================================================
   AI ORB
   ============================================================ */

.ai-orb-area {

    height: 350px;

    display: flex;

    align-items: center;

    justify-content: center;

    position: relative;

}


.ai-orb-area::before {

    content: "";

    position: absolute;

    width: 260px;
    height: 260px;

    border-radius: 50%;

    border:
        1px solid
        rgba(111, 90, 255, 0.25);

    animation:
        orbitRing 8s linear infinite;

}


.ai-orb-area::after {

    content: "";

    position: absolute;

    width: 210px;
    height: 210px;

    border-radius: 50%;

    border:
        1px dashed
        rgba(50, 194, 255, 0.30);

    animation:
        orbitRingReverse 10s linear infinite;

}


.ai-orb {

    position: relative;

    z-index: 3;

    width: 175px;
    height: 175px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: 72px;

    background:

        radial-gradient(
            circle at 32% 22%,
            rgba(255,255,255,0.30),
            transparent 18%
        ),

        linear-gradient(
            145deg,
            #5636d7,
            #20256d 55%,
            #071126
        );

    border:
        2px solid
        rgba(142, 118, 255, 0.70);

    box-shadow:

        0 0 35px
        rgba(101, 69, 255, 0.75),

        0 0 100px
        rgba(41, 130, 255, 0.28),

        inset 0 0 40px
        rgba(133, 104, 255, 0.35);

    animation:
        floatingOrb 4s ease-in-out infinite;

}


@keyframes floatingOrb {

    0%,
    100% {
        transform:
            translateY(0)
            rotate(0deg);
    }

    50% {
        transform:
            translateY(-13px)
            rotate(3deg);
    }

}


@keyframes orbitRing {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }

}


@keyframes orbitRingReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }

}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {

    margin-top: 34px;

    margin-bottom: 16px;

    font-size: 23px;

    font-weight: 850;

    letter-spacing: -0.5px;

}


/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-card {

    position: relative;

    overflow: hidden;

    min-height: 135px;

    padding: 22px;

    border-radius: 22px;

    background:

        linear-gradient(
            145deg,
            rgba(27, 34, 76, 0.90),
            rgba(8, 13, 34, 0.94)
        );

    border:
        1px solid
        rgba(116, 99, 224, 0.25);

    box-shadow:

        0 18px 45px
        rgba(0,0,0,0.25);

    transition:
        transform 0.3s ease,
        border 0.3s ease,
        box-shadow 0.3s ease;

}


.stat-card:hover {

    transform:
        translateY(-7px);

    border-color:
        rgba(123, 108, 255, 0.60);

    box-shadow:

        0 25px 55px
        rgba(67, 48, 180, 0.25);

}


.stat-icon {

    font-size: 25px;

}


.stat-number {

    margin-top: 9px;

    font-size: 25px;

    font-weight: 850;

}


.stat-label {

    margin-top: 3px;

    color: #7e89aa;

    font-size: 11px;

}


/* ============================================================
   QUESTION CARD
   ============================================================ */

.question-card {

    padding: 24px;

    border-radius: 24px;

    background:

        linear-gradient(
            145deg,
            rgba(19, 25, 61, 0.92),
            rgba(6, 10, 29, 0.95)
        );

    border:
        1px solid
        rgba(111, 92, 224, 0.28);

    box-shadow:

        0 22px 60px
        rgba(0,0,0,0.30);

}


/* ============================================================
   INPUT
   ============================================================ */
/* ============================================================
   INPUT
   ============================================================ */

/* Main input container */
div[data-baseweb="input"] {
    background: rgba(8, 15, 35, 0.96) !important;
    border: 1px solid rgba(91, 107, 160, 0.55) !important;
    border-radius: 14px !important;
    min-height: 58px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.20) !important;
    transition: all 0.25s ease !important;
}

/* Input container when focused */
div[data-baseweb="input"]:focus-within {
    border-color: #4da3ff !important;
    box-shadow:
        0 0 0 2px rgba(77, 163, 255, 0.18),
        0 8px 30px rgba(77, 163, 255, 0.15) !important;
}

/* Actual question text */
div[data-baseweb="input"] input {
    background: transparent !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    caret-color: #4da3ff !important;
}

/* Placeholder text */
div[data-baseweb="input"] input::placeholder {
    color: #8fa3c7 !important;
    opacity: 1 !important;
}

/* Question input hover */
div[data-baseweb="input"]:hover {
    border-color: rgba(77, 163, 255, 0.75) !important;
}

/* Remove unwanted white input background */
div[data-baseweb="input"] > div {
    background: transparent !important;
}

/* Remove default Streamlit outline */
div[data-baseweb="input"] input:focus {
    outline: none !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    min-height: 44px;

    border-radius:
        13px !important;

    border:
        1px solid
        rgba(119, 103, 255, 0.35) !important;

    background:

        linear-gradient(
            135deg,
            #5136d7,
            #167ed9
        ) !important;

    color:
        #ffffff !important;

    font-weight:
        750 !important;

    transition:
        all 0.25s ease !important;

}


.stButton > button:hover {

    transform:
        translateY(-2px) !important;

    border-color:
        rgba(145, 133, 255, 0.70) !important;

    box-shadow:

        0 12px 35px
        rgba(68, 65, 255, 0.32) !important;

}


/* ============================================================
   EXAMPLE QUESTIONS
   ============================================================ */

.example-title {

    margin-top: 22px;

    margin-bottom: 10px;

    color:
        #98a3c7;

    font-size:
        12px;

    font-weight:
        750;

}


/* ============================================================
   ANSWER
   ============================================================ */

.answer-container {

    padding: 25px;

    border-radius: 23px;

    background:

        linear-gradient(
            145deg,
            rgba(19, 26, 63, 0.95),
            rgba(7, 11, 30, 0.96)
        );

    border:
        1px solid
        rgba(87, 119, 255, 0.30);

    box-shadow:

        0 20px 60px
        rgba(0,0,0,0.32);

}


.answer-heading {

    display:
        flex;

    align-items:
        center;

    gap:
        12px;

    font-size:
        19px;

    font-weight:
        800;

}


.answer-icon {

    width:
        42px;

    height:
        42px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        13px;

    background:

        linear-gradient(
            135deg,
            #5939ed,
            #138fff
        );

    box-shadow:

        0 0 25px
        rgba(87, 64, 255, 0.35);

}


/* ============================================================
   SOURCE CARDS
   ============================================================ */

.source-card {

    padding:
        17px 20px;

    margin-bottom:
        10px;

    border-radius:
        16px;

    background:
        rgba(19, 25, 57, 0.78);

    border:
        1px solid
        rgba(108, 99, 184, 0.22);

}


.source-number {

    color:
        #7e8cff;

    font-size:
        10px;

    font-weight:
        750;

}


.source-name {

    color:
        #dce2ff;

    font-size:
        14px;

    font-weight:
        700;

}


/* ============================================================
   CHUNK CARDS
   ============================================================ */

.chunk-card {

    padding:
        19px;

    border-radius:
        17px;

    background:
        rgba(7, 11, 29, 0.82);

    border:
        1px solid
        rgba(102, 91, 180, 0.20);

}


.metric {

    display:
        inline-block;

    padding:
        5px 9px;

    margin-right:
        5px;

    border-radius:
        20px;

    background:
        rgba(91, 76, 220, 0.16);

    color:
        #aeb4ff;

    font-size:
        10px;

}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

section[data-testid="stFileUploaderDropzone"] {

    background:
        rgba(15, 21, 49, 0.78) !important;

    border:
        1px dashed
        rgba(111, 96, 220, 0.48) !important;

    border-radius:
        18px !important;

}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    margin-top:
        60px;

    padding-top:
        22px;

    text-align:
        center;

    border-top:
        1px solid
        rgba(120,120,170,0.12);

    color:
        #5f6988;

    font-size:
        11px;

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# END OF PART 1
# ============================================================

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-logo">

        <div class="sidebar-logo-icon">
            🤖
        </div>

        <div class="sidebar-title">
            Enterprise RAG
        </div>

        <div class="sidebar-subtitle">
            AI Knowledge Platform
        </div>

    </div>
    """)

    st.markdown("---")

    st.markdown("### ⚙️ RAG Settings")

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=1,
        max_value=10,
        value=3
    )

    st.markdown("---")

    st.markdown("### 📁 Upload Documents")

    st.caption(
        "Upload PDF, TXT or DOCX files"
    )

    uploaded_files = st.file_uploader(
        "Upload",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:

        st.info(
            f"{len(uploaded_files)} file(s) selected"
        )

        if st.button(
            "🚀 Index Documents",
            use_container_width=True
        ):

            for uploaded_file in uploaded_files:

                try:

                    with st.spinner(
                        f"Indexing {uploaded_file.name}..."
                    ):

                        result = index_uploaded_file(
                            uploaded_file
                        )

                    st.success(
                        f"✓ {result['file_name']} "
                        f"({result['chunks']} chunks)"
                    )

                except Exception as error:

                    st.error(
                        f"Failed: {uploaded_file.name}\n\n"
                        f"{error}"
                    )

    st.markdown("---")

    st.markdown("### 🧠 Technology")

    st.markdown(
        """
**Hybrid RAG Pipeline**

🔹 Python  
🔹 Streamlit  
🔹 ChromaDB  
🔹 BM25  
🔹 RRF Hybrid Retrieval  
🔹 Sentence Transformers  
🔹 Ollama  
🔹 Llama 3.2  
🔹 PDF / DOCX / TXT
"""
    )

    st.markdown("---")

    render_html("""
    <div style="
        display:flex;
        align-items:center;
        gap:8px;
        color:#63e6ad;
        font-size:12px;
        font-weight:700;
        padding:8px 0;
    ">

        <span class="online-dot"></span>

        RAG System Online

    </div>
    """)


# ============================================================
# HERO SECTION
# ============================================================

hero_left, hero_right = st.columns(
    [2.15, 1],
    gap="large"
)


with hero_left:

    render_html("""
    <div class="hero">

        <div class="hero-badge">

            <span class="online-dot"></span>

            SYSTEM ONLINE

        </div>


        <div class="hero-title">

            Your Company Knowledge

            <br>

            <span class="gradient-text">
                Powered by AI
            </span>

        </div>


        <div class="hero-description">

            Upload your enterprise documents and ask questions.
            Our Hybrid RAG pipeline combines semantic search,
            BM25 and Reciprocal Rank Fusion to retrieve relevant
            information and generate grounded answers using Ollama.

        </div>

    </div>
    """)


with hero_right:

    render_html("""
    <div class="ai-orb-area">

        <div class="ai-orb">
            🤖
        </div>

    </div>
    """)


# ============================================================
# RAG SYSTEM OVERVIEW
# ============================================================

render_html("""
<div class="section-title">

    ⚡ RAG System Overview

</div>
""")


stat1, stat2, stat3, stat4 = st.columns(
    4,
    gap="medium"
)


# ------------------------------------------------------------
# STAT 1
# ------------------------------------------------------------

with stat1:

    render_html("""
    <div class="stat-card">

        <div class="stat-icon">
            📚
        </div>

        <div class="stat-number">
            Enterprise
        </div>

        <div class="stat-label">
            Document Knowledge
        </div>

    </div>
    """)


# ------------------------------------------------------------
# STAT 2
# ------------------------------------------------------------

with stat2:

    render_html("""
    <div class="stat-card">

        <div class="stat-icon">
            🔎
        </div>

        <div class="stat-number">
            Hybrid
        </div>

        <div class="stat-label">
            BM25 + Semantic Retrieval
        </div>

    </div>
    """)


# ------------------------------------------------------------
# STAT 3
# ------------------------------------------------------------

with stat3:

    render_html("""
    <div class="stat-card">

        <div class="stat-icon">
            🧠
        </div>

        <div class="stat-number">
            RRF
        </div>

        <div class="stat-label">
            Reciprocal Rank Fusion
        </div>

    </div>
    """)


# ------------------------------------------------------------
# STAT 4
# ------------------------------------------------------------

with stat4:

    render_html("""
    <div class="stat-card">

        <div class="stat-icon">
            ⚡
        </div>

        <div class="stat-number">
            Llama 3.2
        </div>

        <div class="stat-label">
            Local Ollama LLM
        </div>

    </div>
    """)


# ============================================================
# END OF PART 2
# ============================================================

# ============================================================
# QUESTION SECTION
# ============================================================

render_html("""
<div class="section-title">

    🔍 Ask Your Company Knowledge

</div>
""")


render_html("""
<div class="question-card">
""")


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "Ask a Question",
    placeholder="Ask anything about your company documents...",
    key="question_input",
    label_visibility="collapsed"
)


# ============================================================
# ACTION BUTTONS
# ============================================================

ask_col, new_col = st.columns(
    [4, 1],
    gap="small"
)


with ask_col:

    if st.button(
        "🚀  Ask Question",
        use_container_width=True
    ):

        process_question(
            question,
            top_k
        )


with new_col:

    st.button(
        "✨  New Question",
        use_container_width=True,
        on_click=clear_question
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

render_html("""
<div class="example-title">

    💡 TRY THESE QUESTIONS

</div>
""")


example1, example2, example3, example4 = st.columns(
    4,
    gap="small"
)


with example1:

    st.button(
        "What types of leave can employees apply for?",
        use_container_width=True,
        on_click=set_example_question,
        args=(
            "What types of leave can employees apply for?",
        )
    )


with example2:

    st.button(
        "How many vacation days do employees receive?",
        use_container_width=True,
        on_click=set_example_question,
        args=(
            "How many vacation days do employees receive?",
        )
    )


with example3:

    st.button(
        "What is the work from home policy?",
        use_container_width=True,
        on_click=set_example_question,
        args=(
            "What is the work from home policy?",
        )
    )


with example4:

    st.button(
        "How many days in advance should planned leave be submitted?",
        use_container_width=True,
        on_click=set_example_question,
        args=(
            "How many days in advance should planned leave be submitted?",
        )
    )


render_html("""
</div>
""")


# ============================================================
# ANSWER SECTION
# ============================================================

if st.session_state.answer:

    render_html("""
    <div class="section-title">

        🤖 AI Response

    </div>
    """)


    render_html("""
    <div class="answer-container">

        <div class="answer-heading">

            <div class="answer-icon">
                🤖
            </div>

            <div>
                Grounded Answer
            </div>

        </div>

    </div>
    """)


    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    answer_text = st.session_state.answer


    st.markdown(
        f"""
        <div style="
            margin-top:-12px;
            padding:20px 24px;
            background:rgba(13,18,43,0.92);
            border-left:3px solid #6554e8;
            border-right:1px solid rgba(100,90,190,0.18);
            border-bottom:1px solid rgba(100,90,190,0.18);
            border-radius:0 0 18px 18px;
            color:#dce3ff;
            font-size:15px;
            line-height:1.8;
        ">
            {answer_text}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SOURCES / CITATIONS
    # ========================================================

    render_html("""
    <div class="section-title">

        📚 Sources / Citations

    </div>
    """)


    if st.session_state.sources:

        for index, source in enumerate(
            st.session_state.sources,
            start=1
        ):

            render_html(
                f"""
                <div class="source-card">

                    <div class="source-number">
                        SOURCE {index}
                    </div>

                    <div class="source-name">
                        📄 {source}
                    </div>

                </div>
                """
            )

    else:

        render_html("""
        <div class="source-card">

            <div class="source-number">
                SOURCE
            </div>

            <div class="source-name">
                No source name available
            </div>

        </div>
        """)


    # ========================================================
    # RETRIEVED DOCUMENT CHUNKS
    # ========================================================

    if st.session_state.results:

        render_html("""
        <div class="section-title">

            🔎 Retrieved Document Chunks

        </div>
        """)


        for index, result in enumerate(
            st.session_state.results,
            start=1
        ):

            source_name = result.get(
                "source_name"
            )

            if not source_name:

                source_name = clean_source_name(
                    result.get("source", "")
                )


            text = result.get(
                "text",
                ""
            )


            rrf_score = result.get(
                "score",
                0
            )


            bm25_score = result.get(
                "bm25_score",
                0
            )


            semantic_score = result.get(
                "semantic_score",
                0
            )


            with st.expander(
                f"Document {index}  —  {source_name}"
            ):

                render_html(
                    f"""
                    <div class="chunk-card">

                        <div style="
                            margin-bottom:12px;
                            color:#dfe5ff;
                            font-weight:750;
                        ">
                            📄 {source_name}
                        </div>


                        <div style="
                            margin-bottom:15px;
                        ">

                            <span class="metric">
                                RRF: {rrf_score:.5f}
                            </span>

                            <span class="metric">
                                BM25: {bm25_score:.5f}
                            </span>

                            <span class="metric">
                                Semantic: {semantic_score:.5f}
                            </span>

                        </div>


                        <div style="
                            color:#9da8c8;
                            font-size:13px;
                            line-height:1.75;
                            white-space:pre-wrap;
                        ">
                            {text}
                        </div>

                    </div>
                    """
                )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    render_html("""
    <div style="
        margin-top:35px;
        padding:40px 25px;
        text-align:center;
        border-radius:24px;
        background:
            linear-gradient(
                145deg,
                rgba(13,18,43,0.70),
                rgba(5,9,25,0.75)
            );
        border:1px solid rgba(95,85,190,0.16);
    ">

        <div style="
            font-size:46px;
            margin-bottom:12px;
        ">
            🧠
        </div>

        <div style="
            color:#dce3ff;
            font-size:18px;
            font-weight:750;
        ">
            Your enterprise knowledge is ready.
        </div>

        <div style="
            margin-top:8px;
            color:#687494;
            font-size:13px;
        ">
            Ask a question above to retrieve grounded
            information from your documents.
        </div>

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">

    <div style="
        font-size:18px;
        margin-bottom:8px;
    ">
        🤖
    </div>

    <div style="
        color:#8c96b7;
        font-size:12px;
        font-weight:700;
    ">
        Enterprise RAG Pipeline
    </div>

    <div style="
        margin-top:6px;
    ">
        ChromaDB • BM25 • RRF • Sentence Transformers • Ollama
    </div>

    <div style="
        margin-top:8px;
        color:#46506e;
    ">
        Grounded answers from your enterprise documents
    </div>

</div>
""")


# ============================================================
# END OF PART 3
# ============================================================