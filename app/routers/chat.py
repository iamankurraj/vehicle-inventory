from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from app.services.chat_state import get_state, update_state
from app.services.chat_reasoning import reason
from app.services.inventory_query import find_part
from app.services.chat_response import format_inventory_response
from app.services.provider_query import find_providers
from app.services.chat_response import format_provider_response

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("")
def chat(payload: ChatRequest):
    session_id = payload.session_id or str(uuid.uuid4())
    state = get_state(session_id)

    reasoning = reason(payload.message, state)

    # Always update state
    update_state(
        session_id,
        intent=reasoning.get("intent"),
        part=reasoning.get("part"),
        region=reasoning.get("region")
    )

    intent = reasoning.get("intent")

    if intent == "greeting":
        return {
            "session_id": session_id,
            "reply": "Hi! I can help you find spare parts or list providers by region."
        }

    if intent == "help":
        return {
            "session_id": session_id,
            "reply": "Try asking: tyres in Mumbai, or who are the providers in Delhi."
        }

    if reasoning.get("needs_more_info"):
        return {
            "session_id": session_id,
            "reply": reasoning.get("follow_up_question")
        }

    # --------------------------------------------------
    # 3️⃣ LIST PROVIDERS (NEW)
    # --------------------------------------------------

    if intent == "list_providers":
        region = reasoning.get("region")

        providers = find_providers(region)
        reply = format_provider_response(providers, region)

        return {
            "session_id": session_id,
            "reply": reply
        }

    # --------------------------------------------------
    # 4️⃣ SEARCH PART INVENTORY
    # --------------------------------------------------

    if intent == "search_part":
        part = reasoning.get("part")
        region = reasoning.get("region")

        rows = find_part(part, region)
        reply = format_inventory_response(rows, part, region)

        return {
            "session_id": session_id,
            "reply": reply
        }

    # --------------------------------------------------
    # 5️⃣ Fallback
    # --------------------------------------------------

    return {
        "session_id": session_id,
        "reply": "I didn’t quite get that. Could you rephrase?"
    }
