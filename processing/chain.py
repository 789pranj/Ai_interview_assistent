from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from prompts.prompt import GENERAL_PROMPT
from dotenv import load_dotenv
from session.session_memory import add_to_session, get_session_history
import os

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

def run_general_interview(resume_text, user_prompt, session_id="default"):
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.messages import AIMessage, HumanMessage

    import os
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)
    parser = StrOutputParser()

    # Combine all previous messages for context
    history = get_session_history(session_id)
    full_context = ""
    for msg in history:
        role = "user" if isinstance(msg, HumanMessage) else "ai"
        full_context += f"{role}: {msg.content}\n"

    full_context += f"user: {user_prompt}\nresume: {resume_text}"

    from prompts.prompt import GENERAL_PROMPT
    formatted_prompt = GENERAL_PROMPT.format(resume=resume_text, user_prompt=full_context)

    # Generate AI response
    try:
        result = llm.invoke(formatted_prompt)
        parsed_result = parser.parse(str(result))
    except Exception as e:
        parsed_result = f"Error generating AI response: {e}"

    return parsed_result

    