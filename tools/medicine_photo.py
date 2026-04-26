# tools/medicine_photo.py

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


def medicine_photo_analyzer(image_b64: str) -> str:
    prompt = """
Analyze this medicine image and provide:

1. Medicine Name
2. What It Treats
3. When To Use
4. When NOT To Use
5. Common Side Effects
6. Important Warnings

If the medicine is unclear, mention that clearly.

End with:
Always verify with a doctor or pharmacist before use.
"""

    response = requests.post(
        GROQ_URL,
        headers=GROQ_HEADERS,
        data=json.dumps({
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "max_tokens": 700,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ]
        })
    )

    return response.json()["choices"][0]["message"]["content"]