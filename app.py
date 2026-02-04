import streamlit as st
import tempfile
import json

from processing.pdf_loaders import load_pdf
from processing.ocr_loader import load_image_ocr
from processing.chunker import chunk_text
from processing.chain import run_general_interview
from session.session_memory import (
    get_session_history,
    add_to_session,
    clear_session
)
from langchain_core.messages import AIMessage, HumanMessage

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("AI Interview Coach")
st.sidebar.caption("Practice smart • Crack interviews")
st.sidebar.markdown("---")

job_role = st.sidebar.selectbox(
    "Select Job Role",
    ["Software Developer", "Data Analyst", "ML Engineer", "General"]
)

session_id = st.sidebar.text_input(
    "Session ID",
    value="candidate_001"
)

if st.sidebar.button("🧹 Clear Interview"):
    clear_session(session_id)
    st.sidebar.success("Session cleared")

st.sidebar.markdown("---")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>AI Interview Coach</h1>", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF/Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

resume_chunks = None

if uploaded_file:
    suffix = uploaded_file.name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    if suffix == "pdf":
        resume_json = load_pdf(tmp_path)
    else:
        resume_json = load_image_ocr(tmp_path)

    if resume_json:
        # Chunking
        resume_chunks = chunk_text(resume_json["content"])

        # Store chunks temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json",
            mode="w",            
            encoding="utf-8"     
        ) as f:
            json.dump(resume_chunks, f, indent=2)

        temp_json_path = f.name

        st.success("✅ Resume processed & chunked successfully")

        with st.expander("🔍 Preview Resume Chunks"):
            st.json(resume_chunks)
    else:
        st.error("❌ Resume extraction failed")

# ---------------- CHAT HISTORY ----------------
st.markdown("### 💬 Interview Chat")

history = get_session_history(session_id)

for msg in history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("Type your answer..."):
    add_to_session(session_id, HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        thinking = st.empty()
        thinking.markdown("⏳ AI is analyzing...")

        resume_text = (
            "\n".join(chunk["content"] for chunk in resume_chunks)
            if resume_chunks else "No resume provided"
        )

        ai_response = run_general_interview(
            resume_text,
            prompt,
            session_id
        )

        thinking.markdown(ai_response)

    add_to_session(session_id, AIMessage(content=ai_response))
