from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from prompts.prompt import GENERAL_PROMPT
from dotenv import load_dotenv
from session.session_memory import add_to_session, get_session_history
import os

# Load env ONCE
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))


def run_general_interview(resume_text, user_prompt, session_id="default"):
    """
    ChatGPT-style interview:
    - Full memory
    - One question at a time
    - Feedback after every answer
    """

    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )
    parser = StrOutputParser()

    # 🔹 Build full chat history (THIS IS THE MAGIC)
    history = get_session_history(session_id)
    conversation = ""

    for msg in history:
        if isinstance(msg, HumanMessage):
            conversation += f"user: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation += f"ai: {msg.content}\n"

    # Add latest user input
    conversation += f"user: {user_prompt}\n"

    # 🔹 Prepare prompt
    formatted_prompt = GENERAL_PROMPT.format(
        resume=resume_text,
        user_prompt=conversation
    )

    # 🔹 Call LLM
    try:
        result = llm.invoke(formatted_prompt)
        ai_response = parser.parse(str(result.content))
    except Exception as e:
        ai_response = f"⚠️ Error: {e}"

    # 🔹 STORE BOTH USER + AI (CRITICAL)
    add_to_session(session_id, HumanMessage(content=user_prompt))
    add_to_session(session_id, AIMessage(content=ai_response))

    return ai_response
