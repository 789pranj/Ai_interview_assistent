import streamlit as st
from processing.pdf_loaders import load_pdf
from processing.chain import run_general_interview
from session.session_memory import get_session_history, add_to_session, clear_session
from langchain_core.messages import HumanMessage, AIMessage
import tempfile

st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("AI Interview Coach 💼")

session_id = st.text_input("Enter Session ID", value="candidate_001")

# ---------------- PDF Upload ----------------
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
resume_text = None
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name
    resume_text = load_pdf(tmp_path)
    if resume_text:
        st.success("Resume loaded successfully!")
    else:
        st.error("Failed to load resume. Please check your PDF.")

# ---------------- Clear Chat ----------------
if st.button("Clear Chat") and session_id:
    clear_session(session_id)
    st.success(f"Session '{session_id}' cleared!")

# ---------------- Chat ----------------
st.subheader("Interview Chat")

# Display previous messages
history = get_session_history(session_id)
for msg in history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# User input
if prompt := st.chat_input("Type your answer / question here..."):
    # Add user message to session
    add_to_session(session_id, HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # Placeholder for AI typing
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("_AI is typing..._")

        # Generate AI response
        ai_response = run_general_interview(resume_text or "No resume provided", prompt, session_id)

        # Replace typing placeholder with actual response
        typing_placeholder.markdown(ai_response)

    # Save AI response to session
    add_to_session(session_id, AIMessage(content=ai_response))
