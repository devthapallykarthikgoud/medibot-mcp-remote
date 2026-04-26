# tools/symptom_checker.py

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


def symptom_checker(symptoms: str) -> str:
    prompt = f"""
You are a medical assistant.

Patient symptoms: {symptoms}

Give:

1. Possible Conditions (2 to 3)
2. Severity Level (Mild / Moderate / Severe)
3. Home Remedies (3 to 4)
4. OTC Medicine Category
5. When to See a Doctor

End with:
This is not medical advice. Consult a doctor.
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