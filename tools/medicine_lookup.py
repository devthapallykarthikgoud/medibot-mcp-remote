# tools/medicine_lookup.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def medicine_lookup(medicine_name: str) -> str:
    prompt = f"""
You are a pharmacist AI.

Provide information about: {medicine_name}

Give:

1. Medicine Name and Type
2. What It Treats
3. When To Use
4. When NOT To Use
5. Common Side Effects
6. Important Warnings

End with:
Always consult your doctor or pharmacist before use.
"""

    response = requests.post(
        GROQ_URL,
        headers=GROQ_HEADERS,
        data=json.dumps({
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 700,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )

    return response.json()["choices"][0]["message"]["content"]