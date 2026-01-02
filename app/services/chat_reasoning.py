from app.services.gemini import ask_gemini
import json

CANONICAL_PARTS = [
    "damper",
    "brake oil",
    "pads",
    "brake hose kit front",
    "brake hose kit rear",
    "gear oil",
    "chain",
    "sprocket set",
    "springs primary",
    "springs secondary",
    "rim",
    "tyres",
    "tie rod",
    "clevis",
    "dashboard",
    "auxillary lights",
    "battery charger"
]

SYSTEM_PROMPT = f"""
You are Artera Assistant for a vehicle spare parts platform.

Rules:
- Be conversational and natural
- Track what the user wants
- Ask ONLY for missing information
- NEVER ask about vehicle type
- Only care about: part and region
- NEVER invent part names

Allowed canonical parts (EXACT LIST):
{", ".join(CANONICAL_PARTS)}

Mapping rules:
- Convert plurals, typos, and synonyms to the closest canonical part
- Examples:
  - "dampers", "shock absorber" → "damper"
  - "battery chager", "charger" → "battery charger"
- If no close match exists, set part = null

Provider intent rules:
- If the user asks:
  - which providers are in a region
  - list providers in a region
  - who supplies parts in a region
- Then:
  - intent = list_providers
  - region must be extracted
  - part must be null

Output JSON ONLY.

Fields:
- intent: greeting | search_part | list_providers | help | unknown
- part: one of the canonical parts above OR null
- region: string or null
- needs_more_info: true or false
- follow_up_question: string or null

Conversation state:
"""

def reason(message: str, state: dict) -> dict:
    prompt = SYSTEM_PROMPT + f"""
Current state:
{json.dumps(state)}

User message:
{message}
"""

    raw = ask_gemini(prompt)
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()

    try:
        result = json.loads(raw)
    except Exception:
        return {
            "intent": "unknown",
            "part": None,
            "region": None,
            "needs_more_info": True,
            "follow_up_question": "Could you please clarify your request?"
        }

    # -------------------------------
    # Enforce canonical constraints
    # -------------------------------

    if result.get("part") not in CANONICAL_PARTS:
        result["part"] = None

    if result.get("region") == "":
        result["region"] = None

    # -------------------------------
    # Intent-specific follow-up logic
    # -------------------------------

    if result.get("intent") == "search_part":
        if not result.get("part"):
            result["needs_more_info"] = True
            result["follow_up_question"] = "Which spare part are you looking for?"
        elif not result.get("region"):
            result["needs_more_info"] = True
            result["follow_up_question"] = "Which region should I check?"
        else:
            result["needs_more_info"] = False
            result["follow_up_question"] = None

    elif result.get("intent") == "list_providers":
        result["part"] = None  # providers do not require part

        if not result.get("region"):
            result["needs_more_info"] = True
            result["follow_up_question"] = "Which region should I list providers for?"
        else:
            result["needs_more_info"] = False
            result["follow_up_question"] = None

    else:
        result["needs_more_info"] = False
        result["follow_up_question"] = None

    return result
