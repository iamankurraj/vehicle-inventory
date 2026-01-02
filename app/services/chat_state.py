# Simple in-memory session store
chat_sessions = {}

def get_state(session_id: str) -> dict:
    return chat_sessions.setdefault(session_id, {
        "intent": None,
        "part": None,
        "region": None
    })

def update_state(session_id: str, **kwargs):
    state = get_state(session_id)
    for k, v in kwargs.items():
        state[k] = v

