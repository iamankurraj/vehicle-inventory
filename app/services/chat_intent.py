from app.services.gemini import ask_gemini
import json

INTENT_PROMPT = """
You are Artera Assistant, a chatbot for a vehicle spare parts platform.

Classify the user's intent and extract entities.

Respond ONLY in JSON.

Allowed intents:
- greeting        (hello, hi, good morning, etc.)
- help            (what can you do, how does this work)
- search_part     (asking about part availability)
- unknown

Fields:
- intent
- part (nullable)
- region (nullable)

User message:
"""


def parse_intent(message: str) -> dict:
    raw = ask_gemini(INTENT_PROMPT + message)

    try:
        return json.loads(raw)
    except Exception:
        return {"intent": "unknown", "part": None, "region": None}
