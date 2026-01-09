from langchain_core.messages import AIMessage, HumanMessage

sessions = {}

def add_to_session(session_id, message):
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append(message)

def get_session_history(session_id):
    return sessions.get(session_id, [])

def clear_session(session_id):
    sessions[session_id] = []
