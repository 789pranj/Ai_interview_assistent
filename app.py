import streamlit as st
from processing.pdf_loaders import load_pdf
from processing.chain import run_general_interview
from session.session_memory import get_session_history, add_to_session, clear_session
from langchain_core.messages import AIMessage, HumanMessage
import tempfile

st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide",
)

st.sidebar.title("AI Interview Coach")
st.sidebar.caption("Practice smart • Crack interviews")

st.sidebar.markdown("---")

job_role = st.sidebar.selectbox(
    "Select Job Role",
    ["Software Developer", "Data Analyst", "ML Engineer", "General"]
)

st.sidebar.markdown(
    """
    ### 📌 Instructions
    • Upload your resume (PDF)  
    • Answer honestly  
    • Ask follow-up questions  
    • Get AI feedback in real time  
    """
)

st.sidebar.markdown("---")

session_id = st.sidebar.text_input(
    "Session ID",
    value="candidate_001",
    help="Use same ID to continue interview"
)

if st.sidebar.button("🧹 Clear Interview"):
    clear_session(session_id)
    st.sidebar.success("Session cleared")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + LangChain")

st.markdown(
    """
    <h1 style='text-align: center;'>AI Interview Coach</h1>
    <p style='text-align: center; color: gray;'>
    Personalized interview practice powered by AI
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("### 📄 Resume Upload")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type="pdf",
    label_visibility="collapsed"
)

resume_text = None
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    resume_text = load_pdf(tmp_path)

    if resume_text:
        st.success("✅ Resume loaded successfully")
    else:
        st.error("❌ Failed to read resume")

st.info(f"🧠 **Session:** `{session_id}`  |  **Role:** `{job_role}`")

st.markdown("### 💬 Interview Chat")

history = get_session_history(session_id)

for msg in history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input("Type your answer or question..."):
    add_to_session(session_id, HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        thinking = st.empty()
        thinking.markdown("⏳ _AI is analyzing your response..._")

        ai_response = run_general_interview(
            resume_text or "No resume provided",
            prompt,
            session_id
        )

        thinking.markdown(ai_response)

    add_to_session(session_id, AIMessage(content=ai_response))
