from processing.pdf_loaders import load_pdf
from processing.chain import run_general_interview
from session.session_memory import get_session_history, clear_session
from langchain_core.messages import AIMessage, HumanMessage

pdf_path = "Pranjal_Resume.pdf"
resume_text = load_pdf(pdf_path)

if not resume_text:
    print("Failed to load resume.")
    exit()

session_id = "candidate_001"
print(f"\nStarting interview session: {session_id}\n")

prompts = [
    "Ask 3 technical questions based on my resume.",
    "Ask 2 follow-up questions on coding skills.",
    "Provide feedback in 5 bullet points on my strengths and weaknesses."
]

for i, user_prompt in enumerate(prompts, start=1):
    print(f"\n--- User Prompt {i} ---\n{user_prompt}\n")
    
    response = run_general_interview(resume_text, user_prompt, session_id=session_id)
    print(f"\n--- AI Response {i} ---\n{response}\n")

print("\n--- Full Session History ---")
history = get_session_history(session_id)
for msg in history:
    role = "USER" if isinstance(msg, HumanMessage) else "AI"
    print(f"{role}: {msg.content}\n")

