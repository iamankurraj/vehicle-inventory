# import os
# from google import genai

# from dotenv import load_dotenv
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise RuntimeError("GEMINI_API_KEY not set in environment")

# # Create Gemini client
# client = genai.Client(api_key=GEMINI_API_KEY)

# def ask_gemini(prompt: str) -> str:
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )
#     return response.text.strip()
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def ask_gemini(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
