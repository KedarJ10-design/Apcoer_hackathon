"""
📝 Handwritten Notes Intelligence Assistant — Premium Streamlit App

A beautiful, local-first RAG system that reads handwritten PDF notes,
understands them, and answers questions based ONLY on the information
contained in those notes.
"""

import streamlit as st
import time
from pathlib import Path

# ── Page Configuration ─────────────────────────────────────
st.set_page_config(
    page_title="Handwritten Notes AI",
    page_icon=":material/edit_document:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

    * { font-family: 'Inter', sans-serif !important; }

    /* Theme Variables */
    :root {
        --bg-primary: #0a0a0f;
        --bg-sidebar: linear-gradient(180deg, #0d0d14 0%, #111122 100%);
        --text-primary: #f1f5f9;
        --text-secondary: #64748b;
        --accent: #6366f1;
        --accent-border: rgba(99, 102, 241, 0.15);
        --card-bg: rgba(255, 255, 255, 0.02);
        --card-border: rgba(255, 255, 255, 0.06);
    }
    
    [data-theme="light"] {
        --bg-primary: #f8fafc;
        --bg-sidebar: #ffffff;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --accent: #4f46e5;
        --accent-border: #e2e8f0;
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
    }

    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    [data-testid="stSidebar"] {
        background: var(--bg-sidebar);
        border-right: 1px solid var(--accent-border);
    }

    /* Hero */
    .hero {
        background: var(--card-bg);
        border: 1px solid var(--accent-border);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero h1 {
        color: var(--text-primary);
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        position: relative;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 0;
        position: relative;
    }

    /* Glass Card */
    .glass {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Welcome Card */
    .welcome {
        text-align: center;
        padding: 4rem 2rem;
        background: var(--card-bg);
        border: 1px solid var(--accent-border);
        border-radius: 20px;
    }
    .welcome h2 { color: var(--text-primary); font-weight: 800; }
    .welcome p { color: var(--text-secondary); line-height: 1.8; font-size: 1.05rem; }
    .welcome .steps {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    .step-pill {
        background: var(--pill-bg);
        border: 1px solid var(--card-border);
        border-radius: 100px;
        padding: 0.5rem 1.25rem;
        color: var(--text-primary);
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Native Streamlit Chat adjustments */
    [data-testid="stChatMessage"] {
        background-color: var(--chat-bg) !important;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    
    /* Source Tags */
    .sources {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px solid var(--card-border);
    }
    .src-tag {
        background: var(--tag-bg);
        border: 1px solid var(--tag-border);
        color: var(--tag-text);
        border-radius: 8px;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Context Preview */
    .context-preview {
        background: var(--card-bg);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
        color: var(--text-secondary);
        font-size: 0.82rem;
        line-height: 1.5;
        max-height: 120px;
        overflow-y: auto;
    }

    /* Stats */
    .stat-box {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .stat-box .num {
        color: var(--text-primary);
        font-size: 1.6rem;
        font-weight: 700;
    }
    .stat-box .label {
        color: var(--text-secondary);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: var(--tag-bg);
        border: 1px solid var(--tag-border);
        color: var(--tag-text);
        border-radius: 100px;
        padding: 0.25rem 0.75rem;
        font-size: 0.7rem;
        font-weight: 600;
    }

    /* Sidebar styling */
    .sidebar-title {
        color: var(--text-primary);
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }

    .privacy-note {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.7rem;
        padding: 1rem 0;
        border-top: 1px solid var(--card-border);
        margin-top: 1rem;
    }
    
    /* Quick Actions */
    .quick-actions-title {
        color: var(--text-secondary);
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    }
</style>
""", unsafe_allow_html=True)

# ── Dynamic Theme Switching ─────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.sidebar.markdown('<div class="sidebar-title">:material/palette: Theme Toggle</div>', unsafe_allow_html=True)
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button(":material/dark_mode: Dark", use_container_width=True):
        st.session_state.theme = "dark"
        st.rerun()
with col2:
    if st.button(":material/light_mode: Light", use_container_width=True):
        st.session_state.theme = "light"
        st.rerun()

st.components.v1.html(f"""
    <script>
        const doc = window.parent.document;
        doc.documentElement.setAttribute('data-theme', '{st.session_state.theme}');
    </script>
""", height=0, width=0)


# ── Session State ──────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False
if "pages_data" not in st.session_state:
    st.session_state.pages_data = []
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0
if "total_pages" not in st.session_state:
    st.session_state.total_pages = 0
if "ocr_time" not in st.session_state:
    st.session_state.ocr_time = 0


# ── Processing Pipeline ───────────────────────────────────
def process_pdf(uploaded_file):
    """Full ingestion pipeline with detailed progress bar."""
    from src.ocr_pipeline import pdf_to_images, ocr_image, clean_text, save_ocr_results
    from src.vector_db import chunk_pages, ingest_chunks, clear_collection
    from src.config import UPLOAD_DIR

    file_path = UPLOAD_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    progress = st.progress(0)
    status = st.empty()
    eta = st.empty()
    start = time.time()

    # Step 1: PDF → Images
    status.markdown(":material/bolt: **Step 1/4** — Converting PDF to images...")
    images = pdf_to_images(str(file_path))
    total = len(images)
    progress.progress(10)

    # Step 2: OCR each page
    pages = []
    ocr_start = time.time()
    for i, img in enumerate(images):
        pn = i + 1
        progress.progress(10 + int((pn / total) * 55))
        status.markdown(f":material/search: **Step 2/4** — Reading page **{pn}/{total}**...")
        if i > 0:
            avg = (time.time() - ocr_start) / i
            rem = int(avg * (total - i))
            eta.markdown(f":material/timer: ~**{rem // 60}m {rem % 60}s** remaining")
        raw = ocr_image(img)
        pages.append({"page": pn, "text": clean_text(raw)})
    eta.empty()

    save_ocr_results(pages, uploaded_file.name.replace(".pdf", ""))
    st.session_state.pages_data = pages
    st.session_state.total_pages = total

    # Step 3: Chunk
    progress.progress(70)
    status.markdown(":material/package: **Step 3/4** — Chunking text...")
    clear_collection()
    chunks = chunk_pages(pages)

    # Step 4: Embed
    progress.progress(80)
    status.markdown(f":material/psychology: **Step 4/4** — Indexing **{len(chunks)}** chunks...")
    count = ingest_chunks(chunks, uploaded_file.name.replace(".pdf", ""))
    st.session_state.total_chunks = count

    # Done
    progress.progress(100)
    elapsed = time.time() - start
    st.session_state.ocr_time = elapsed
    status.markdown(f":material/check_circle: **Done!** {total} pages → {count} chunks in **{int(elapsed)}s**")
    st.session_state.document_loaded = True
    return total, count


def ask_question(question: str):
    """Retrieve + Generate."""
    from src.vector_db import search
    from src.llm_engine import generate_answer
    results = search(question)
    return generate_answer(question, results)


# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title"><span class="material-symbols-rounded" style="vertical-align: -0.2em; font-size: 1.2em;">description</span> Upload Notes</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    if uploaded:
        if st.button(":material/rocket_launch: Process PDF", use_container_width=True, type="primary"):
            try:
                pages, chunks = process_pdf(uploaded)
                st.success(f"✅ {pages} pages, {chunks} chunks ready!", icon="✅")
                st.session_state.needs_summary = True
            except Exception as e:
                st.error(f"❌ {e}", icon="❌")

    st.markdown("---")

    if st.session_state.document_loaded:
        st.markdown('<div class="sidebar-title"><span class="material-symbols-rounded" style="vertical-align: -0.2em; font-size: 1.2em;">bar_chart</span> Stats</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="num">{st.session_state.total_pages}</div><div class="label">Pages</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><div class="num">{st.session_state.total_chunks}</div><div class="label">Chunks</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-box"><div class="num">{int(st.session_state.ocr_time)}s</div><div class="label">Time</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        show_context = st.toggle("Show source text", value=True)
    else:
        st.info("Upload a PDF to get started.", icon="ℹ️")
        show_context = True

    st.markdown("---")

    if st.button(":material/delete: Wipe Database & Cache", use_container_width=True):
        from src.vector_db import clear_collection
        import shutil
        from src.config import OCR_OUTPUT_DIR
        clear_collection()
        if OCR_OUTPUT_DIR.exists():
            shutil.rmtree(OCR_OUTPUT_DIR)
            OCR_OUTPUT_DIR.mkdir()
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    st.markdown(
        '<div class="privacy-note"><span class="material-symbols-rounded" style="vertical-align: -0.2em; font-size: 1.1em;">lock</span> 100% Local & Private<br>Powered by Ollama + ChromaDB</div>',
        unsafe_allow_html=True,
    )


# ── Main ───────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1><span class="material-symbols-rounded" style="vertical-align: -0.1em; font-size: 1.1em;">edit_document</span> Handwritten Notes AI</h1>
    <p>Upload handwritten PDF notes · Ask questions in plain English · Get AI answers with source citations</p>
</div>
""", unsafe_allow_html=True)


if not st.session_state.document_loaded:
    st.markdown("""
    <div class="welcome">
        <h2><span class="material-symbols-rounded" style="vertical-align: -0.1em; font-size: 1.1em;">waving_hand</span> Welcome</h2>
        <p>Upload your scanned handwritten notes and ask questions.<br>
        The AI reads your writing, indexes it, and answers from your notes only.</p>
        <div class="steps">
            <span class="step-pill">1. Upload PDF</span>
            <span class="step-pill">2. OCR reads text</span>
            <span class="step-pill">3. Text indexed</span>
            <span class="step-pill">4. Ask anything</span>
            <span class="step-pill">5. AI answers</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    def stream_response(text):
        for chunk in text.split(" "):
            yield chunk + " "
            time.sleep(0.04)

    # 1. Chat history
    for i, msg in enumerate(st.session_state.chat_history):
        with st.chat_message(msg["role"]):
            if msg.get("is_typing"):
                st.write_stream(stream_response(msg["content"]))
                st.session_state.chat_history[i]["is_typing"] = False
            else:
                st.markdown(msg["content"])

            if msg.get("sources"):
                html = '<div class="sources">'
                for s in msg["sources"]:
                    html += f'<span class="src-tag">📄 Page {s["page"]} · {s["score"]}</span>'
                html += '</div>'

                # Context preview
                if show_context:
                    html += '<div class="context-preview"><strong>Retrieved text:</strong><br>'
                    for s in msg["sources"][:2]:
                        html += f'<em>[Page {s["page"]}]</em> {s["text"][:200]}...<br><br>'
                    html += '</div>'
                    
                st.markdown(html, unsafe_allow_html=True)
                
    # 2. Auto-Summary Execution
    if st.session_state.get("needs_summary"):
        st.session_state.needs_summary = False
        with st.chat_message("assistant"):
            with st.spinner(":material/auto_awesome: Generating executive summary..."):
                resp = ask_question("Please provide a concise 3-bullet summary of the main topics in these notes.")
                
                full_text = f":material/auto_awesome: **I have finished reading your notes!** Here is a quick summary:\n\n{resp['answer']}"
                st.write_stream(stream_response(full_text))
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": full_text,
                    "sources": resp.get("sources", []),
                    "is_typing": False
                })

    # Quick Actions
    if st.session_state.chat_history:
        st.markdown('<div class="quick-actions-title"><span class="material-symbols-rounded" style="vertical-align: -0.2em; font-size: 1.2em;">bolt</span> Quick Actions</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(":material/edit_document: Summarize Notes", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": "Summarize these notes for me."})
                st.session_state.needs_answer = True
                st.session_state.current_question = "Summarize these notes for me."
                st.rerun()
        with c2:
            if st.button(":material/key: Key Takeaways", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": "What are the 3 main key takeaways from this document?"})
                st.session_state.needs_answer = True
                st.session_state.current_question = "What are the 3 main key takeaways from this document?"
                st.rerun()
        with c3:
            if st.button(":material/help: Quiz Me", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": "Ask me a quiz question based on these notes to test my knowledge."})
                st.session_state.needs_answer = True
                st.session_state.current_question = "Ask me a short quiz question based on these notes to test my knowledge."
                st.rerun()
        
    # 3. Handle normal user input
    question = st.chat_input("Ask about your notes...")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.needs_answer = True
        st.session_state.current_question = question
        st.rerun()
        
    if st.session_state.get("needs_answer"):
        st.session_state.needs_answer = False
        q = st.session_state.current_question
        with st.chat_message("assistant"):
            with st.spinner(":material/psychology: Thinking..."):
                try:
                    resp = ask_question(q)
                    st.write_stream(stream_response(resp["answer"]))
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": resp["answer"],
                        "sources": resp.get("sources", []),
                        "is_typing": False
                    })
                except Exception as e:
                    err_msg = f":material/warning: Error: {str(e)}"
                    st.markdown(err_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": err_msg,
                        "sources": [],
                        "is_typing": False
                    })

