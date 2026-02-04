import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from session.session_memory import get_session_history
from prompts.prompt import GENERAL_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

def run_general_interview(resume_text, user_prompt, session_id):

    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    parser = StrOutputParser()
    history = get_session_history(session_id)

    conversation = ""
    for msg in history:
        role = "user" if isinstance(msg, HumanMessage) else "ai"
        conversation += f"{role}: {msg.content}\n"

    conversation += f"user: {user_prompt}\n"

    prompt = GENERAL_PROMPT.format(
        resume=resume_text,
        user_prompt=conversation
    )

    try:
        response = llm.invoke(prompt)
        return parser.parse(str(response.content))
    except Exception as e:
        return f"⚠️ Error: {e}"
